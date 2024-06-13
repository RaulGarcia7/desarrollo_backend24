const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/actividad_2')
    .then(() => console.log('Conectado a la Base de Datos'))
    .catch((error) => console.error(error))