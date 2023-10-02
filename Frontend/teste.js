const elementosDiv = document.querySelector('#wanteds')

async function listWanted() {
    try {
        const retorno = await fetch('http://localhost:8080/wanteds');
        if (!retorno.ok) {
            throw new Error('Erro na requisição');
        }

        const wanteds = await retorno.json();
        if (wanteds && wanteds.potential_matches && wanteds.potential_matches.length > 0) {
            wanteds.potential_matches.forEach(wanted => {
                preecher(wanted);
            });
        } else {
            console.error('A resposta da API não possui propriedade potential_matches ou está vazia.');
        }
    } catch (error) {
        console.error('Ocorreu um erro:', error);
    }
}


function preecher(wanted) {
    if (wanted) {
    
        const wantedHTML = `
        <div id="wanteds">
            <p>Wanted_origin_id: ${wanted.wanted_origin_id} </p>
            <p>Charges: ${wanted.charges}</p>
            <p>Nationality: ${wanted.nationality}</p>
            <p>dates_of_birth_used: ${wanted.dates_of_birth_used}</p>
            <p>distinguishing_marks: ${wanted.distinguishing_marks}</p>
            <p>eyes_color: ${wanted.eyes_color}</p>
            <p>forename: ${wanted.forename}</p>
            <p>hair_color: ${wanted.hair_color}</p>
            <p>height: ${wanted.height}</p>
            <p>images: ${wanted.images}</p>
            <p>issuing_country_id: ${wanted.issuing_country_id}</p>
            <p>languages: ${wanted.languages}</p>
            <p>name: ${wanted.name}</p>
            <p>place_of_birth: ${wanted.place_of_birth}</p>
            <p>sex: ${wanted.sex}</p>
            <p>weight: ${wanted.weight}</p>
            <p>wanted_origin: ${wanted.wanted_origin}</p>
            <p>age_range: ${wanted.age_range}</p>
            <p>aliases: ${wanted.aliases}</p>
            <p>ncic: ${wanted.ncic}</p>
            <p>age_max: ${wanted.age_max}</p>
            <p>age_min: ${wanted.age_min}</p>
            <p>build: ${wanted.build}</p>
            <p>complexion: ${wanted.complexion}</p>
            <p>details: ${wanted.details}</p>
            <p>eyes_raw: ${wanted.eyes_raw}</p>
            <p>field_offices: ${wanted.field_offices}</p>
            <p>hair_raw: ${wanted.hair_raw}</p>
            <p>height_max: ${wanted.height_max}</p>
            <p>height_min: ${wanted.height_min}</p>
            <p>modified: ${wanted.modified}</p>
            <p>occupations: ${wanted.occupations}</p>
            <p>person_classification: ${wanted.person_classification}</p>
            <p>possible_countries: ${wanted.possible_countries}</p>
            <p>possible_states: ${wanted.possible_states}</p>
            <p>poster_classification: ${wanted.poster_classification}</p>
            <p>publication: ${wanted.publication}</p>
            <p>race: ${wanted.race}</p>
            <p>race_raw: ${wanted.race_raw}</p>
            <p>remarks: ${wanted.remarks}</p>
            <p>reward_text: ${wanted.reward_text}</p>
            <p>status: ${wanted.status}</p>
            <p>subjects: ${wanted.subjects}</p>
            <p>suspects: ${wanted.suspects}</p>
            <p>title: ${wanted.title}</p>
            <p>url: ${wanted.url}</p>
            <p>warning_message: ${wanted.warning_message}</p>
            <p>weight_max: ${wanted.weight_max}</p>
            <p>weight_min: ${wanted.weight_min}</p>
            <p>analyzed_at: ${wanted.analyzed_at}</p>
        </div>
        `;
        elementosDiv.innerHTML += wantedHTML;
    }else {
        console.error('Objeto wanted é nulo.');
    }
}

function searchById() {
    const searchInput = document.getElementById('searchInput').value;
    const elementosDiv = document.querySelector('#wanteds');

    // Certifique-se de que o ID seja válido antes de realizar a pesquisa
    if (searchInput.trim() !== '') {
        const matchedWanted = findWantedById(searchInput);
        if (matchedWanted) {
            // Limpe a div antes de adicionar o resultado
            elementosDiv.innerHTML = '';
            preecher(matchedWanted);
        } else {
            elementosDiv.innerHTML = 'Registro não encontrado.';
        }
    } else {
        elementosDiv.innerHTML = 'Por favor, digite um ID válido.';
    }
}

// Função para encontrar um registro pelo ID
function findWantedById(id) {
    // Percorra a lista de wanteds e retorne o registro correspondente ao ID
    for (const wanted of wanteds.potential_matches) {
        if (wanted.wanted_origin_id === id) {
            return wanted;
        }
    }
    return null; // Retorne null se não encontrar o registro
}



listWanted()