import React from 'react';

const LoginForm = () => {
  const handleGitHubRedirect = () => {
    const clientId = 'TU_GITHUB_CLIENT_ID'; // Mismo que usaste en Django
    const redirectUri = 'http://localhost:5173/'; 
    // scope=user:email solicita permiso específico para leer el correo
    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email`;
    
    // Redirección dura nativa
    window.location.href = githubAuthUrl;
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      <h2>Sistema Pokedex - Acceso Requerido</h2>
      <p>Debes autenticar tu identidad en GitHub para continuar.</p>
      <button 
        onClick={handleGitHubRedirect}
        style={{ padding: '12px 24px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#24292e', color: 'white', border: 'none', borderRadius: '5px' }}
      >
        Ingresar con GitHub
      </button>
    </div>
  );
};

export default LoginForm;