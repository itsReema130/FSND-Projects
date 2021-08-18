/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-2z-rt5ew.us.auth0.com', // the auth0 domain prefix
    audience: 'cafe', // the audience set for the auth0 app
    clientId: 'FtSJ2GXabTK6pFbygK9nR89TN4xQiMrr', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};

// https://dev-2z-rt5ew.us.auth0.com/authorize?audience=cafe&response_type=token&client_id=epCvSx8zyOADECUWPtQfXVNwftTlOYrf&redirect_uri=http://localhost:8100