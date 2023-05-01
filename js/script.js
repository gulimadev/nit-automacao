document.addEventListener('DOMContentLoaded', function(){
    var nitNumero = document.getElementById('nit');
    var name = document.getElementById('name');
    var cpf = document.getElementById('cpf');
    var dataNasc = document.getElementById('dataNasc');
    fetch('nit.json')
    .then(function(response){
        return response.json();
    })
    .then(function(nit){
        nitNumero.textContent = nit.nit;
        name.textContent = nit.name;
        cpf.textContent = nit.cpf;
        dataNasc.textContent = nit.dataNasc;
    })
    .catch(function(error){

        console.error('Error ao tentar abrir json:', error);
    });
});
