const functions = require('@google-cloud/functions-framework');
const { BigQuery } = require('@google-cloud/bigquery');
const admin = require('firebase-admin');
const serviceAccount = require('./unischedule-5ee93-firebase-adminsdk-ci6y9-6cde344deb.json');

// Inicializar la aplicación de Firebase
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();
const bigquery = new BigQuery();

const datasetId = 'unischedule_bq'; // Reemplaza con el ID de tu dataset en BigQuery
const tableId = 'BQ52'; // Reemplaza con el ID de tu tabla en BigQuery

// Función para insertar datos en BigQuery
async function insertDataIntoBigQuery(rows) {
  const options = {
    skipInvalidRows: true, // Opcional: omite filas inválidas
    ignoreUnknownValues: true // Opcional: ignora valores desconocidos en filas
  };
  console.log("Voy a intentar conectarme a BQ");

  // Insertar los datos en la tabla de BigQuery
  await bigquery.dataset(datasetId).table(tableId).insert(rows, options);
  console.log(`Insertadas ${rows.length} filas en BigQuery`);
}

// Función para obtener datos de las reuniones
async function getMeetingsData() {
  console.log("Obteniendo datos de las reuniones");
  try {
    const meetingsData = [];
    const meetingsSnapshot = await db.collection('Meetings').get();

    for (const meetingDoc of meetingsSnapshot.docs) {
      const meetingData = meetingDoc.data();

      // Obtener los datos de las evaluaciones
      const evaluationsSnapshot = await meetingDoc.ref.collection('Evaluations').get();
      const evaluationsData = evaluationsSnapshot.docs.map(doc => doc.data());

      // Calcular el promedio de OverallSatisfactionScore
      let overallSatisfactionScore = null;
      if (evaluationsData.length > 0) {
        const satisfactionScores = evaluationsData.map(evaluation => evaluation.OverallSatisfactionScore);
        overallSatisfactionScore = satisfactionScores.reduce((acc, score) => acc + score, 0) / satisfactionScores.length;
      }

      // Obtener los datos del usuario
      const userID = meetingData.UserID;
      const userDoc = await db.collection('Users').doc(userID).get();
      const userData = userDoc.data();

      // Construir la entrada transformada
      const transformedEntry = {
        UserID: userID,
        UserType: userData ? userData.UserType : null,
        UserSemester: userData ? userData.UserSemester : null,
        UserCareer: userData ? userData.UserCareer : null,
        MeetingDate: new Date(meetingData.MeetingDate).toISOString().slice(0, 10),  //TODO workaround para las fechas
        DayOfWeek: meetingData.DayOfWeek,
        MeetingStartTime: meetingData.MeetingStartTime?.slice(0,2),  // TODO: Workaround since data is HH:MM:DD and we expect it to be half intervals like 16:30
        MeetingDuration: meetingData.MeetingDuration,
        MeetingBuilding: meetingData.MeetingBuilding,
        MeetingPurpose: meetingData.MeetingPurpose,
        OverallSatisfactionScore: overallSatisfactionScore
      };

      meetingsData.push(transformedEntry);
    }

    // Después de obtener los datos de las reuniones, enviarlos a BigQuery
    await insertDataIntoBigQuery(meetingsData);
    return meetingsData;
  } catch (error) {
    throw error;
  }
}

// Definir la función HTTP 'helloHttp'
functions.http('helloHttp', (req, res) => {
  getMeetingsData()
    .then(meetingsData => {
      console.log('Datos de Reuniones:', meetingsData);
      res.send(meetingsData);
    })
    .catch(error => {
      console.error('Error al obtener datos de reuniones:', error);
      res.status(500).send(error);
    });
});
