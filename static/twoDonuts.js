(()=>{"use strict";var e,t,n,r,o={},s={};function a(e){var t=s[e];if(void 0!==t)return t.exports;var n=s[e]={exports:{}};return o[e](n,n.exports,a),n.exports}function i(){}function c(e){return e()}function l(e){e.forEach(c)}function u(e){return"function"==typeof e}a.m=o,t=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,a.t=function(n,r){if(1&r&&(n=this(n)),8&r)return n;if("object"==typeof n&&n){if(4&r&&n.__esModule)return n;if(16&r&&"function"==typeof n.then)return n}var o=Object.create(null);a.r(o);var s={};e=e||[null,t({}),t([]),t(t)];for(var i=2&r&&n;"object"==typeof i&&!~e.indexOf(i);i=t(i))Object.getOwnPropertyNames(i).forEach((e=>s[e]=()=>n[e]));return s.default=()=>n,a.d(o,s),o},a.d=(e,t)=>{for(var n in t)a.o(t,n)&&!a.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},a.f={},a.e=e=>Promise.all(Object.keys(a.f).reduce(((t,n)=>(a.f[n](e,t),t)),[])),a.u=e=>"chunk."+e+".js",a.miniCssF=e=>{},a.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),a.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),n={},r="expense:",a.l=(e,t,o,s)=>{if(n[e])n[e].push(t);else{var i,c;if(void 0!==o)for(var l=document.getElementsByTagName("script"),u=0;u<l.length;u++){var d=l[u];if(d.getAttribute("src")==e||d.getAttribute("data-webpack")==r+o){i=d;break}}i||(c=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,a.nc&&i.setAttribute("nonce",a.nc),i.setAttribute("data-webpack",r+o),i.src=e),n[e]=[t];var p=(t,r)=>{i.onerror=i.onload=null,clearTimeout(f);var o=n[e];if(delete n[e],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((e=>e(r))),t)return t(r)},f=setTimeout(p.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=p.bind(null,i.onerror),i.onload=p.bind(null,i.onload),c&&document.head.appendChild(i)}},a.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e;a.g.importScripts&&(e=a.g.location+"");var t=a.g.document;if(!e&&t&&(t.currentScript&&(e=t.currentScript.src),!e)){var n=t.getElementsByTagName("script");if(n.length)for(var r=n.length-1;r>-1&&!e;)e=n[r--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),a.p=e})(),(()=>{var e={555:0};a.f.j=(t,n)=>{var r=a.o(e,t)?e[t]:void 0;if(0!==r)if(r)n.push(r[2]);else{var o=new Promise(((n,o)=>r=e[t]=[n,o]));n.push(r[2]=o);var s=a.p+a.u(t),i=new Error;a.l(s,(n=>{if(a.o(e,t)&&(0!==(r=e[t])&&(e[t]=void 0),r)){var o=n&&("load"===n.type?"missing":n.type),s=n&&n.target&&n.target.src;i.message="Loading chunk "+t+" failed.\n("+o+": "+s+")",i.name="ChunkLoadError",i.type=o,i.request=s,r[1](i)}}),"chunk-"+t,t)}};var t=(t,n)=>{var r,o,[s,i,c]=n,l=0;if(s.some((t=>0!==e[t]))){for(r in i)a.o(i,r)&&(a.m[r]=i[r]);c&&c(a)}for(t&&t(n);l<s.length;l++)o=s[l],a.o(e,o)&&e[o]&&e[o][0](),e[o]=0},n=self.webpackChunkexpense=self.webpackChunkexpense||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))})(),new Set;const d="undefined"!=typeof window?window:"undefined"!=typeof globalThis?globalThis:global;class p{constructor(e){this.options=e,this._listeners="WeakMap"in d?new WeakMap:void 0}observe(e,t){return this._listeners.set(e,t),this._getObserver().observe(e,this.options),()=>{this._listeners.delete(e),this._observer.unobserve(e)}}_getObserver(){var e;return null!==(e=this._observer)&&void 0!==e?e:this._observer=new ResizeObserver((e=>{var t;for(const n of e)p.entries.set(n.target,n),null===(t=this._listeners.get(n.target))||void 0===t||t(n)}))}}p.entries="WeakMap"in d?new WeakMap:void 0,new Map;let f,h=[];new Set,new Set,new Set(["allowfullscreen","allowpaymentrequest","async","autofocus","autoplay","checked","controls","default","defer","disabled","formnovalidate","hidden","inert","ismap","loop","multiple","muted","nomodule","novalidate","open","playsinline","readonly","required","reversed","selected"]),"function"==typeof HTMLElement&&(f=class extends HTMLElement{constructor(){super(),this.attachShadow({mode:"open"})}connectedCallback(){const{on_mount:e}=this.$$;this.$$.on_disconnect=e.map(c).filter(u);for(const e in this.$$.slotted)this.appendChild(this.$$.slotted[e])}attributeChangedCallback(e,t,n){this[e]=n}disconnectedCallback(){l(this.$$.on_disconnect)}$destroy(){(function(e,t){const n=e.$$;null!==n.fragment&&(function(e){const t=[],n=[];h.forEach((r=>-1===e.indexOf(r)?t.push(r):n.push(r))),n.forEach((e=>e())),h=t}(n.after_update),l(n.on_destroy),n.fragment&&n.fragment.d(t),n.on_destroy=n.fragment=null,n.ctx=[])})(this,1),this.$destroy=i}$on(e,t){if(!u(t))return i;const n=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return n.push(t),()=>{const e=n.indexOf(t);-1!==e&&n.splice(e,1)}}$set(e){var t;this.$$set&&(t=e,0!==Object.keys(t).length)&&(this.$$.skip_bound=!0,this.$$set(e),this.$$.skip_bound=!1)}});const b=["#008FFB","#00E396","#FEB019","#FF4560","#775DD0","#4caf50","#546E7A","#f9a3a4","#F86624","#662E9B","#2E294E","#5A2A27","#D7263D"],m=document.getElementById("user-currency").textContent,g=JSON.parse(document.getElementById("expense-by-category").textContent),y=JSON.parse(document.getElementById("expense-by-account").textContent);function v(e,t){const n=Object.values(e).map((e=>parseFloat(e))),r=n.reduce(((e,t)=>e+t),0);return console.log(e),console.log(n),{dataLabels:{formatter:function(e,t){return`${m} ${(e*r/100).toFixed(2)}`}},chart:{type:t},series:n,labels:Object.keys(e),legend:{show:!1},tooltip:{y:{formatter:e=>`${(e/r*100).toFixed(2)}%`}},colors:b}}console.log(Object.values(g).map((e=>parseFloat(e))));const $=new Intl.NumberFormat("en-US",{style:"currency",currency:m});function w(e){const t=Object.values(e).map((e=>parseFloat(e))).reduce(((e,t)=>e+t),0);let n="",r=0;for(const o of Object.keys(e)){const s=`color: white; background-color: ${b[r]}`,a=(e[o]/t*100).toFixed(0);n+=`<span>\n            <span class=badge rounded-pill style="${s}">${o}</span>&nbsp;\n            ${$.format(e[o])}\n        <span class="text-secondary">${a}%</span>\n        </span>&nbsp;`,r>=b.length-1?r=0:r+=1}return n}window.addEventListener("load",(()=>{a.e(927).then(a.t.bind(a,927,23)).then((e=>{const t=e.default;new t(document.getElementById("category-chart"),v(g,"donut")).render(),document.getElementById("category-chart-legend").innerHTML=w(g),new t(document.getElementById("account-chart"),v(y,"pie")).render(),document.getElementById("account-chart-legend").innerHTML=w(y)}))}))})();
