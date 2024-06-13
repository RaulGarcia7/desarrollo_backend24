const http = require('http');


class ClassError extends Error {
    constructor(message = '') {
        super();
        this.message = message;
    }
}

const fetchPokedexData = async () => {
    const url = 'https://raw.githubusercontent.com/fanzeyi/pokemon.json/master/pokedex.json'

    const fetchResult = await fetch(url);

    if (fetchResult.ok) {
        return await fetchResult.json();
    }

    throw new ClassError('Se ha producido un error'); // Uso de excepción como ErrorBoundary o try/catch en caso de no fetch de data

};

const handleRequest = async (req, res) => {
    const pokedexData = await fetchPokedexData();
    const urlPokemon = req.url.substring(1).split('/')
    let pokemonData;

    if (urlPokemon.length === 1) {
        const idOrName = urlPokemon[0];
        if (!isNaN(idOrName)) { // Si es un número se identifica como id
            const pokemonId = parseInt(idOrName);
            pokemonData = pokedexData.find(pokemon => pokemon.id === pokemonId);
        } else {
            const pokemonName = decodeURI(idOrName).toLowerCase(); 
            pokemonData = pokedexData.find(pokemon => {
                const names = Object.values(pokemon.name).map(name => name.toLowerCase()); //name es un objeto con varios idiomas de nombres. hacemos array y recorremos
                return names.includes(pokemonName)
            });
        }
    }


    if (pokemonData) {
        const response = {
            'Tipo': pokemonData.type,
            'HP': pokemonData.base.HP,
            'Attack': pokemonData.base.Attack,
            'Defense': pokemonData.base.Defense,
            'Sp. Attack': pokemonData.base['Sp. Attack'],
            'Sp. Defense': pokemonData.base['Sp. Defense'],
            'Speed': pokemonData.base.Speed
        }

        res.writeHead(200, { 'Content-Type': 'text/plain' })
        res.end(JSON.stringify(response, null, 7))
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end("Este pokemon no existe")
    }
};

const server = http.createServer(handleRequest)

server.listen(3000, () => {
    console.log("escuchando el 3000")
});
