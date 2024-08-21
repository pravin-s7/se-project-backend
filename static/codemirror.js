/* codemirror.js */

/* CodeMirror library - download from https://codemirror.net/ or use CDN */
(function() {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.8/codemirror.min.js';
    script.onload = function() {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.8/codemirror.min.css';
      document.head.appendChild(link);
    };
    document.head.appendChild(script);
})();
  