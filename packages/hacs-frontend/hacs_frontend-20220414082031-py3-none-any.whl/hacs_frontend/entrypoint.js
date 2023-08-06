
try {
  new Function("import('/hacsfiles/frontend/main-79b6d9fd.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-79b6d9fd.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  