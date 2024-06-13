const axios = require('axios')
const express = require('express');
const mongoose = require('mongoose');


const app = express();
const port = 3000;
require('./database')

app.use(express.json())

// Schema para nuestra bd
const favSongsSchema = new mongoose.Schema({
    name: String,
    artist: String,
    release_date: String,
    duration: String,
});


const FavoriteSongs = mongoose.model('FavoriteSongs', favSongsSchema);

//Rutas

app.post('/favorite-songs', async (req, res) => {
    try {
        const existingSongsCount = await FavoriteSongs.countDocuments();
        
        if (existingSongsCount >= 5) {
            return res.status(400).json({ message: "Ya hay 5 canciones favoritas en la base de datos. Utiliza el método PUT para actualizarlas." });
        }

        const topTracks = await getTopTracks();
        
        for (const track of topTracks) {
            const { name, artist, release_date, duration } = track;
            const newFavoriteSong = new FavoriteSongs({
                name: name,
                artist: artist,
                release_date: release_date,
                duration: duration
            });
            await newFavoriteSong.save();
        }
        
        res.status(200).json({ message: "Canciones favoritas guardadas con éxito." });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Se ha producido un error al agregar las canciones favoritas" });
    }
});


app.get('/favorite-songs', async (req, res) => {
    try {
        const songs = await FavoriteSongs.find();
        const message = "Este es tu top 5 canciones escuchadas en las últimas 4 semanas:"
        res.status(200).json({ message: message, songs: songs });
    } catch (error) {
        res.status(500).json({error: error.message})
    }
});


app.put('/favorite-songs', async (req, res)=> {
    try {
        const topTracksUpdated = await getTopTracks();

        // Obtenemos los nombres de las canciones y artistas de la lista actualizada
        const updatedSongs = topTracksUpdated.map(track => ({ name: track.name, artist: track.artist }));

        // Eliminamos las canciones que no están en la lista actualizada
        await FavoriteSongs.deleteMany({
            $or: updatedSongs.map(song => ({
                $and: [
                    { name: song.name },
                    { artist: song.artist }
                ]
            }))
        });

        // Insertamos las canciones que no están en la base de datos
        for (const track of topTracksUpdated) {
            const { name, artist, release_date, duration } = track;
            await FavoriteSongs.updateOne(
                { name: name, artist: artist, release_date: release_date, duration: duration },
                { $set: track },
                { upsert: true }
            );
        }

        res.status(200).json(topTracksUpdated);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Error en la actualización de las canciones" });
    }
});


app.delete('/favorite-songs', async (req, res) => {
    try {
        await FavoriteSongs.deleteMany();
        res.status(200).json({message: "Se han eliminado todas las canciones favoritas"})
    } catch {
        res.status(500).json({error: "No se han podido borrar las canciones"})
    }
});

const token = '[Access-Token]';

async function getTopTracks() {
    try {
        const response = await axios.get('https://api.spotify.com/v1/me/top/tracks', {
            headers: {
                'Authorization': `Bearer ${token}`, 
                'Content-Type': 'application/json',
            },
            params: {
                'time_range': 'short_term',
                'limit': '5',
            }
        });
        // Mapeo de la respuesta
        const data = response.data.items.map(({ name, artists, album, duration_ms }) => {
        
            const minutes = Math.floor(duration_ms / 60000);
            const seconds = ((duration_ms % 60000) / 1000).toFixed(0);
            const duration = `${minutes}:${(seconds < 10 ? '0' : '')}${seconds}`; 

            // Retornar el objeto con los datos transformados
            return {
                name: name,
                artist: artists.map(artist => artist.name).join(', '),
                release_date: album.release_date,
                duration: duration
            };
        });
        return data;
    } catch (error) {
        console.error(error);
        return { error: error.message };
    }
}


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });