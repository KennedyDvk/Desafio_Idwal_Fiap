const showData = (result) =>{
    for(const tabela in result) {
        if (document.querySelector("#"+tabela)) {
            document.querySelector("#"+tabela).value = result[tabela]
        }

    }
}

var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
        // Faça uma requisição HTTP GET para a sua API de backend
        fetch(`http://localhost:8080/wanteds`, {
            method: 'GET',
            mode: 'cors',
            // Adicione qualquer cabeçalho necessário aqui (por exemplo, content-type)
        })
        .then(data => showData(data))
        .then(response => response.json())
        .then(data => {
            // Manipule os dados da resposta e atualize seu HTML
            let dadosProcurados = data; // Ajuste isso com base na estrutura da resposta da sua API
            atualizarUI(dadosProcurados);
        })
        .catch(error => {
            console.error('Erro:', error);
        });

        // Função para atualizar a interface do usuário com dados do backend
        /*function atualizarUI(data) {
            // Modifique os elementos HTML com os dados recebidos
            let tabela = document.getElementById('tabela');
            tabela.innerHTML = `
                <p>Nome: ${data.nome}</p>
                <p>ID: ${data.id}</p>
                <p>Altura: ${data.altura}</p>
                <p>Peso: ${data.peso}</p>
                <p>Data de Nascimento: ${data.dataNascimento}</p>
                
            `;
        }*/


  /*fetch("http://localhost:8080?wanted_origin_id") // Use o URL correto do seu endpoint
    .then(response => response.json())
    .then(data => {
        const tabela = document.getElementById('tabela');
        const dados = data; // A resposta JSON contém diretamente os dados desejados

        // Crie uma tabela HTML para exibir os dados
        const table = document.createElement('table');
        table.classList.add('table'); // Adicione classes de estilo conforme necessário

        // Crie a primeira linha da tabela com cabeçalhos
        const headerRow = table.insertRow(0);
        const headers = Object.keys(dados[0]); // Assumindo que todos os objetos têm a mesma estrutura

        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });

        // Preencha a tabela com os dados
        dados.forEach(item => {
            const row = table.insertRow();
            headers.forEach(header => {
                const cell = row.insertCell();
                cell.textContent = item[header];
            });
        });

        // Limpe o conteúdo anterior da tabela e adicione a nova tabela
        tabela.innerHTML = '';
        tabela.appendChild(table);
    })
    .catch(error => {
        console.error('Erro ao buscar itens:', error);
    });*/


/*fetch()
    .then(response => response.json())
    .then(result => console.log(result))
    .then(function(data) {
        let dados = data.result;
        console.log(dados)
      })
      .catch(function(error) {
        console.log(error);
      });*/


     
    