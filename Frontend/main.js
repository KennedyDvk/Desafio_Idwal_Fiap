

var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

fetch("https://dummyjson.com/user/1")
    .then(response => response.json())
    .then(result => console.log(result))
    .then(function(data) {
        let dados = data.result;
        console.log(dados)
      })
      .catch(function(error) {
        console.log(error);
      });
    