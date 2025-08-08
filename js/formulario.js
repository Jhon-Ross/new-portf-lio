document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-contato');
    const mensagemErro = document.getElementById('mensagem-erro'); // Elemento para exibir erros

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Captura os dados do formulário
        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const mensagem = document.getElementById('mensagem').value;

        // Cria um objeto com os dados
        const formData = {
            nome: nome,
            email: email,
            mensagem: mensagem
        };

        // ✅ Substitua pela URL real do seu backend na Railway:
        fetch('https://backend-portf-lio-production.up.railway.app/enviar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message);
                form.reset();
            } else {
                if (mensagemErro) {
                    mensagemErro.textContent = data.message;
                } else {
                    alert(data.message);
                }
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            if (mensagemErro) {
                mensagemErro.textContent = 'Ocorreu um erro ao enviar a mensagem. Tente novamente.';
            } else {
                alert('Ocorreu um erro ao enviar a mensagem. Tente novamente.');
            }
        });
    });
});
