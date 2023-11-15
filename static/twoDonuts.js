(()=>{"use strict";var e,t,r,n,o={},a={};function c(e){var t=a[e];if(void 0!==t)return t.exports;var r=a[e]={exports:{}};return o[e](r,r.exports,c),r.exports}c.m=o,t=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,c.t=function(r,n){if(1&n&&(r=this(r)),8&n)return r;if("object"==typeof r&&r){if(4&n&&r.__esModule)return r;if(16&n&&"function"==typeof r.then)return r}var o=Object.create(null);c.r(o);var a={};e=e||[null,t({}),t([]),t(t)];for(var s=2&n&&r;"object"==typeof s&&!~e.indexOf(s);s=t(s))Object.getOwnPropertyNames(s).forEach((e=>a[e]=()=>r[e]));return a.default=()=>r,c.d(o,a),o},c.d=(e,t)=>{for(var r in t)c.o(t,r)&&!c.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},c.f={},c.e=e=>Promise.all(Object.keys(c.f).reduce(((t,r)=>(c.f[r](e,t),t)),[])),c.u=e=>"chunk."+e+".js",c.miniCssF=e=>{},c.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),c.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r={},n="expense:",c.l=(e,t,o,a)=>{if(r[e])r[e].push(t);else{var s,l;if(void 0!==o)for(var i=document.getElementsByTagName("script"),u=0;u<i.length;u++){var d=i[u];if(d.getAttribute("src")==e||d.getAttribute("data-webpack")==n+o){s=d;break}}s||(l=!0,(s=document.createElement("script")).charset="utf-8",s.timeout=120,c.nc&&s.setAttribute("nonce",c.nc),s.setAttribute("data-webpack",n+o),s.src=e),r[e]=[t];var p=(t,n)=>{s.onerror=s.onload=null,clearTimeout(f);var o=r[e];if(delete r[e],s.parentNode&&s.parentNode.removeChild(s),o&&o.forEach((e=>e(n))),t)return t(n)},f=setTimeout(p.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=p.bind(null,s.onerror),s.onload=p.bind(null,s.onload),l&&document.head.appendChild(s)}},c.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e;c.g.importScripts&&(e=c.g.location+"");var t=c.g.document;if(!e&&t&&(t.currentScript&&(e=t.currentScript.src),!e)){var r=t.getElementsByTagName("script");if(r.length)for(var n=r.length-1;n>-1&&!e;)e=r[n--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),c.p=e})(),(()=>{var e={555:0};c.f.j=(t,r)=>{var n=c.o(e,t)?e[t]:void 0;if(0!==n)if(n)r.push(n[2]);else{var o=new Promise(((r,o)=>n=e[t]=[r,o]));r.push(n[2]=o);var a=c.p+c.u(t),s=new Error;c.l(a,(r=>{if(c.o(e,t)&&(0!==(n=e[t])&&(e[t]=void 0),n)){var o=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\n("+o+": "+a+")",s.name="ChunkLoadError",s.type=o,s.request=a,n[1](s)}}),"chunk-"+t,t)}};var t=(t,r)=>{var n,o,[a,s,l]=r,i=0;if(a.some((t=>0!==e[t]))){for(n in s)c.o(s,n)&&(c.m[n]=s[n]);l&&l(c)}for(t&&t(r);i<a.length;i++)o=a[i],c.o(e,o)&&e[o]&&e[o][0](),e[o]=0},r=self.webpackChunkexpense=self.webpackChunkexpense||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();const s=document.getElementById("user-currency").textContent,l=["#008FFB","#00E396","#FEB019","#FF4560","#775DD0","#4caf50","#546E7A","#f9a3a4","#F86624","#662E9B","#2E294E","#5A2A27","#D7263D"],i=new Intl.NumberFormat("en-US",{style:"currency",currency:s});function u(e,t){const r=Object.values(e).map((e=>parseFloat(e))),n=r.reduce(((e,t)=>e+t),0);return{dataLabels:{formatter:function(e,t){const r=parseFloat((e*n/100).toFixed(2));return`${i.format(r)}`}},chart:{type:t},series:r,labels:Object.keys(e),legend:{show:!1},tooltip:{y:{formatter:e=>`${(e/n*100).toFixed(2)}%`}},colors:l}}function d(e){const t=Object.values(e).map((e=>parseFloat(e))).reduce(((e,t)=>e+t),0);let r="",n=0;for(const o of Object.keys(e)){const a=`color: white; background-color: ${l[n]}`,c=(e[o]/t*100).toFixed(1);r+=`<small class="text-nowrap p-1 text-small">\n            <span class=badge rounded-pill style="${a}">${o}</span>\n            &nbsp;${i.format(e[o])}\n        <span class="text-secondary">${c}%</span>\n        </small>`,n>=l.length-1?n=0:n+=1}return r}const p=JSON.parse(document.getElementById("expense-by-category").textContent),f=JSON.parse(document.getElementById("expense-by-account").textContent);window.addEventListener("load",(()=>{c.e(927).then(c.t.bind(c,927,23)).then((e=>{const t=e.default;new t(document.getElementById("category-chart"),u(p,"donut")).render(),document.getElementById("category-chart-legend").innerHTML=d(p),new t(document.getElementById("account-chart"),u(f,"pie")).render(),document.getElementById("account-chart-legend").innerHTML=d(f)}))}))})();
