var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/core/css/estilos.css',
    '/static/core/img/logo.png',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
      fetch(event.request)
      .then(function(result){
        return caches.open(CACHE_NAME)
        .then(function(c){
          c.put(event.request.url, result.clone());
          return result;
        })
      })
      .catch(function(es){
        return caches.match(event.request)
      })
    );
});

/*self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {

          return fetch(event.request)
          .catch(function(rsp) {
             return response; 
          });
          
          
        })
    );
});


//solo para cachear todo reemplazar por esta versión del Fetch


self.addEventListener('fetch', function(event) {
    event.respondWith(

      fetch(event.request)
      .then((result)=>{
        return caches.open(CACHE_NAME)
        .then(function(c) {
          c.put(event.request.url, result.clone())
          return result;
        })
        
      })
      .catch(function(e){
          return caches.match(event.request)
      })
  

     
    );
});
*/
// codigo para notificaciones push
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var firebaseConfig = {
  apiKey: "AIzaSyBMFNTBGqbym8y1-EhA44yq3E3GpgRvgng",
  authDomain: "cineland-fc1ba.firebaseapp.com",
  projectId: "cineland-fc1ba",
  storageBucket: "cineland-fc1ba.appspot.com",
  messagingSenderId: "578919981495",
  appId: "1:578919981495:web:7c7318b7c03af518488832"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){

  /*let title = 'titulo de la notificacion'
  let options = {
      body: 'Este es el mensaje',
      icon: '/static/core/img/logo.png'
  }*/

  console.log("Ha llegado la notificacion")
  let title = payload.notification.title;
  let options = {
      body: payload.notification.body,
      icon: payload.notification.icon
  }
  self.registration.showNotification(title, options)
})