(()=>{"use strict";function t(){}function e(t){return t()}function n(){return Object.create(null)}function o(t){t.forEach(e)}function r(t){return"function"==typeof t}function s(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}let c;function l(t,e){return c||(c=document.createElement("a")),c.href=e,t===c.href}function a(t){return 0===Object.keys(t).length}function i(e,...n){if(null==e)return t;const o=e.subscribe(...n);return o.unsubscribe?()=>o.unsubscribe():o}function u(t,e,n){t.$$.on_destroy.push(i(e,n))}new Set;const d="undefined"!=typeof window?window:"undefined"!=typeof globalThis?globalThis:global;class p{constructor(t){this.options=t,this._listeners="WeakMap"in d?new WeakMap:void 0}observe(t,e){return this._listeners.set(t,e),this._getObserver().observe(t,this.options),()=>{this._listeners.delete(t),this._observer.unobserve(t)}}_getObserver(){var t;return null!==(t=this._observer)&&void 0!==t?t:this._observer=new ResizeObserver((t=>{var e;for(const n of t)p.entries.set(n.target,n),null===(e=this._listeners.get(n.target))||void 0===e||e(n)}))}}p.entries="WeakMap"in d?new WeakMap:void 0;let f,h=!1;function m(t,e){t.appendChild(e)}function g(t,e,n){t.insertBefore(e,n||null)}function $(t){t.parentNode&&t.parentNode.removeChild(t)}function b(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function y(t){return document.createElement(t)}function x(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function v(t){return document.createTextNode(t)}function w(){return v(" ")}function _(t,e,n,o){return t.addEventListener(e,n,o),()=>t.removeEventListener(e,n,o)}function k(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function E(t,e){e=""+e,t.data!==e&&(t.data=e)}function M(t,e){t.value=null==e?"":e}function C(t,e,n,o){null==n?t.style.removeProperty(e):t.style.setProperty(e,n,o?"important":"")}function T(t){f=t}new Map;const L=[],S=[];let O=[];const A=[],H=Promise.resolve();let N=!1;function B(t){O.push(t)}const D=new Set;let F=0;function I(){if(0!==F)return;const t=f;do{try{for(;F<L.length;){const t=L[F];F++,T(t),j(t.$$)}}catch(t){throw L.length=0,F=0,t}for(T(null),L.length=0,F=0;S.length;)S.pop()();for(let t=0;t<O.length;t+=1){const e=O[t];D.has(e)||(D.add(e),e())}O.length=0}while(L.length);for(;A.length;)A.pop()();N=!1,D.clear(),T(t)}function j(t){if(null!==t.fragment){t.update(),o(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(B)}}const z=new Set;let q,J;function R(t,e){t&&t.i&&(z.delete(t),t.i(e))}function W(t,e,n,o){if(t&&t.o){if(z.has(t))return;z.add(t),q.c.push((()=>{z.delete(t),o&&(n&&t.d(1),o())})),t.o(e)}else o&&o()}function P(t){t&&t.c()}function U(t,n,s,c){const{fragment:l,after_update:a}=t.$$;l&&l.m(n,s),c||B((()=>{const n=t.$$.on_mount.map(e).filter(r);t.$$.on_destroy?t.$$.on_destroy.push(...n):o(n),t.$$.on_mount=[]})),a.forEach(B)}function X(t,e){const n=t.$$;null!==n.fragment&&(function(t){const e=[],n=[];O.forEach((o=>-1===t.indexOf(o)?e.push(o):n.push(o))),n.forEach((t=>t())),O=e}(n.after_update),o(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function G(e,r,s,c,l,a,i,u=[-1]){const d=f;T(e);const p=e.$$={fragment:null,ctx:[],props:a,update:t,not_equal:l,bound:n(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(r.context||(d?d.$$.context:[])),callbacks:n(),dirty:u,skip_bound:!1,root:r.target||d.$$.root};i&&i(p.root);let m=!1;if(p.ctx=s?s(e,r.props||{},((t,n,...o)=>{const r=o.length?o[0]:n;return p.ctx&&l(p.ctx[t],p.ctx[t]=r)&&(!p.skip_bound&&p.bound[t]&&p.bound[t](r),m&&function(t,e){-1===t.$$.dirty[0]&&(L.push(t),N||(N=!0,H.then(I)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}(e,t)),n})):[],p.update(),m=!0,o(p.before_update),p.fragment=!!c&&c(p.ctx),r.target){if(r.hydrate){h=!0;const t=(g=r.target,Array.from(g.childNodes));p.fragment&&p.fragment.l(t),t.forEach($)}else p.fragment&&p.fragment.c();r.intro&&R(e.$$.fragment),U(e,r.target,r.anchor,r.customElement),h=!1,I()}var g;T(d)}new Set(["allowfullscreen","allowpaymentrequest","async","autofocus","autoplay","checked","controls","default","defer","disabled","formnovalidate","hidden","inert","ismap","loop","multiple","muted","nomodule","novalidate","open","playsinline","readonly","required","reversed","selected"]),"function"==typeof HTMLElement&&(J=class extends HTMLElement{constructor(){super(),this.attachShadow({mode:"open"})}connectedCallback(){const{on_mount:t}=this.$$;this.$$.on_disconnect=t.map(e).filter(r);for(const t in this.$$.slotted)this.appendChild(this.$$.slotted[t])}attributeChangedCallback(t,e,n){this[t]=n}disconnectedCallback(){o(this.$$.on_disconnect)}$destroy(){X(this,1),this.$destroy=t}$on(e,n){if(!r(n))return t;const o=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return o.push(n),()=>{const t=o.indexOf(n);-1!==t&&o.splice(t,1)}}$set(t){this.$$set&&!a(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}});class Y{$destroy(){X(this,1),this.$destroy=t}$on(e,n){if(!r(n))return t;const o=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return o.push(n),()=>{const t=o.indexOf(n);-1!==t&&o.splice(t,1)}}$set(t){this.$$set&&!a(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}const K=[];function Q(e,n=t){let o;const r=new Set;function c(t){if(s(e,t)&&(e=t,o)){const t=!K.length;for(const t of r)t[1](),K.push(t,e);if(t){for(let t=0;t<K.length;t+=2)K[t][0](K[t+1]);K.length=0}}}return{set:c,update:function(t){c(t(e))},subscribe:function(s,l=t){const a=[s,l];return r.add(a),1===r.size&&(o=n(c)||t),s(e),()=>{r.delete(a),0===r.size&&o&&(o(),o=null)}}}}const V=Q([]),Z=Q(!0),tt=Q(""),et=function(e,n,s){const c=!Array.isArray(e),l=c?[e]:e,a=n.length<2;return{subscribe:Q(void 0,(e=>{let s=!1;const u=[];let d=0,p=t;const f=()=>{if(d)return;p();const o=n(c?u[0]:u);a?e(o):p=r(o)?o:t},h=l.map(((t,e)=>i(t,(t=>{u[e]=t,d&=~(1<<e),s&&f()}),(()=>{d|=1<<e}))));return s=!0,f(),function(){o(h),p(),s=!1}})).subscribe}}([Z,tt,V],(([t,e,n])=>{let o=[];return o=t?n:n.filter((t=>t.expense)),e&&(o=o.filter((t=>t.description.toLowerCase().includes(e.toLowerCase())))),o})),nt=Q(0);function ot(t){const e=new Date(t);return`${e.getDate()} ${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][e.getMonth()]}`}function rt(t,e,n){const o=t.slice();return o[4]=e[n],o}function st(t){let e,n,o,r,s,c;return{c(){e=x("svg"),n=x("path"),o=x("path"),r=x("path"),s=x("path"),c=x("path"),k(n,"stroke","none"),k(n,"d","M0 0h24v24H0z"),k(n,"fill","none"),k(o,"d","M14 3v4a1 1 0 0 0 1 1h4"),k(r,"d","M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"),k(s,"d","M9 17h6"),k(c,"d","M9 13h6"),k(e,"xmlns","http://www.w3.org/2000/svg"),k(e,"class","text-primary"),k(e,"width","12"),k(e,"height","12"),k(e,"viewBox","0 0 24 24"),k(e,"stroke-width","2"),k(e,"stroke","currentColor"),k(e,"fill","none"),k(e,"stroke-linecap","round"),k(e,"stroke-linejoin","round")},m(t,l){g(t,e,l),m(e,n),m(e,o),m(e,r),m(e,s),m(e,c)},d(t){t&&$(e)}}}function ct(t){let e,n,o,r,s,c,l,a,i,u,d,p,f,h,b,x,M,C,T,L=t[4].description+"",S=t[1].format(t[4].amount)+"",O=t[4].account+"",A=ot(t[4].created_at)+"",H=t[4].expense&&st();function N(){return t[3](t[4])}return{c(){e=y("tr"),n=y("td"),o=v(L),r=w(),H&&H.c(),l=w(),a=y("td"),i=v(S),d=w(),p=y("td"),f=v(O),h=w(),b=y("td"),x=v(A),M=w(),k(n,"data-bs-toggle",s=t[4].expense?"modal":""),k(n,"data-bs-target",c=t[4].expense?"#expense-modal":""),k(a,"class",u="DEBIT"===t[4].action?"text-danger":"text-success"),k(p,"class","d-none d-lg-block")},m(t,s){g(t,e,s),m(e,n),m(n,o),m(n,r),H&&H.m(n,null),m(e,l),m(e,a),m(a,i),m(e,d),m(e,p),m(p,f),m(e,h),m(e,b),m(b,x),m(e,M),C||(T=_(e,"click",N),C=!0)},p(e,r){t=e,1&r&&L!==(L=t[4].description+"")&&E(o,L),t[4].expense?H||(H=st(),H.c(),H.m(n,null)):H&&(H.d(1),H=null),1&r&&s!==(s=t[4].expense?"modal":"")&&k(n,"data-bs-toggle",s),1&r&&c!==(c=t[4].expense?"#expense-modal":"")&&k(n,"data-bs-target",c),1&r&&S!==(S=t[1].format(t[4].amount)+"")&&E(i,S),1&r&&u!==(u="DEBIT"===t[4].action?"text-danger":"text-success")&&k(a,"class",u),1&r&&O!==(O=t[4].account+"")&&E(f,O),1&r&&A!==(A=ot(t[4].created_at)+"")&&E(x,A)},d(t){t&&$(e),H&&H.d(),C=!1,T()}}}function lt(e){let n,o,r,s,c,l=e[0],a=[];for(let t=0;t<l.length;t+=1)a[t]=ct(rt(e,l,t));return{c(){n=y("div"),o=y("table"),r=y("thead"),r.innerHTML='<tr><th scope="col">Description</th> \n                <th scope="col">Amount</th> \n                <th class="d-none d-lg-block" scope="col">Account</th> \n                <th scope="col">Date</th></tr>',s=w(),c=y("tbody");for(let t=0;t<a.length;t+=1)a[t].c();k(o,"class","table table-hover"),k(n,"class","card-body")},m(t,e){g(t,n,e),m(n,o),m(o,r),m(o,s),m(o,c);for(let t=0;t<a.length;t+=1)a[t]&&a[t].m(c,null)},p(t,[e]){if(3&e){let n;for(l=t[0],n=0;n<l.length;n+=1){const o=rt(t,l,n);a[n]?a[n].p(o,e):(a[n]=ct(o),a[n].c(),a[n].m(c,null))}for(;n<a.length;n+=1)a[n].d(1);a.length=l.length}},i:t,o:t,d(t){t&&$(n),b(a,t)}}}function at(t,e,n){let o;u(t,et,(t=>n(0,o=t)));let{currency:r=""}=e;const s=new Intl.NumberFormat("en-US",{style:"currency",currency:r});return t.$$set=t=>{"currency"in t&&n(2,r=t.currency)},[o,s,r,t=>{t.expense&&nt.set(t.id)}]}const it=class extends Y{constructor(t){super(),G(this,t,at,lt,s,{currency:2})}};function ut(e){let n,r,s,c,l,a,i,u,d,p,f,h,b;return{c(){n=y("div"),r=v("Show "),s=v(e[1]),c=v("'s:\n    "),l=y("button"),a=v("Transactions"),u=w(),d=y("button"),p=v("Expenses"),k(l,"class",i=e[0]?dt:pt),k(d,"class",f=e[0]?pt:dt),k(n,"class","col-md-8 col-sm-12 mt-2 text-sm-start text-md-end")},m(t,o){g(t,n,o),m(n,r),m(n,s),m(n,c),m(n,l),m(l,a),m(n,u),m(n,d),m(d,p),h||(b=[_(l,"click",e[2]),_(d,"click",e[3])],h=!0)},p(t,[e]){1&e&&i!==(i=t[0]?dt:pt)&&k(l,"class",i),1&e&&f!==(f=t[0]?pt:dt)&&k(d,"class",f)},i:t,o:t,d(t){t&&$(n),h=!1,o(b)}}}const dt="ms-1 btn btn-primary btn-sm",pt="ms-1 btn btn-outline-secondary btn-sm";function ft(t,e,n){let o;u(t,Z,(t=>n(0,o=t)));const r=(new Date).toLocaleString("default",{month:"long"});return[o,r,()=>Z.set(!0),()=>Z.set(!1)]}const ht=class extends Y{constructor(t){super(),G(this,t,ft,ut,s,{})}};function mt(e){let n,o,r,s;return{c(){n=y("div"),o=y("input"),k(o,"class","form-control"),k(o,"placeholder","Search transactions..."),k(o,"type","search"),k(o,"name","search"),k(o,"id","search"),k(n,"class","col-md-4 col-sm-12 mt-2")},m(t,c){g(t,n,c),m(n,o),M(o,e[0]),r||(s=_(o,"input",e[1]),r=!0)},p(t,[e]){1&e&&o.value!==t[0]&&M(o,t[0])},i:t,o:t,d(t){t&&$(n),r=!1,s()}}}function gt(t,e,n){let o;return u(t,tt,(t=>n(0,o=t))),[o,function(){o=this.value,tt.set(o)}]}const $t=class extends Y{constructor(t){super(),G(this,t,gt,mt,s,{})}};function bt(t,e,n){const o=t.slice();return o[3]=e[n],o}function yt(e){let n,o,r,s,c,l,a,i,u,d,p;return{c(){n=y("h1"),n.innerHTML='<span class="placeholder col-2"></span> \n                        <span class="placeholder col-5"></span>',o=w(),r=y("p"),r.innerHTML='<span class="placeholder col-2"></span> \n                        <span class="placeholder col-3"></span>',s=w(),c=y("p"),c.innerHTML='<span class="placeholder col-2"></span> \n                        <span class="placeholder col-1"></span> \n                        <span class="placeholder col-3"></span>',l=w(),a=y("p"),a.innerHTML='<span class="placeholder col-3"></span> \n                        <span class="placeholder col-3"></span>',i=w(),u=y("p"),u.innerHTML='<span class="placeholder col-3"></span> \n                        <span class="placeholder col-1"></span> \n                        <span class="placeholder col-4"></span>',d=w(),p=y("div"),k(n,"class","modal-title fs-5 mb-3 placeholder-glow"),k(n,"id","expense-modal-label"),k(r,"class","placeholder-glow"),k(c,"class","placeholder-glow"),k(a,"class","placeholder-glow"),k(u,"class","placeholder-glow"),k(p,"class","img-thumbnail mb-2"),C(p,"width","100px"),C(p,"height","100px")},m(t,e){g(t,n,e),g(t,o,e),g(t,r,e),g(t,s,e),g(t,c,e),g(t,l,e),g(t,a,e),g(t,i,e),g(t,u,e),g(t,d,e),g(t,p,e)},p:t,d(t){t&&$(n),t&&$(o),t&&$(r),t&&$(s),t&&$(c),t&&$(l),t&&$(a),t&&$(i),t&&$(u),t&&$(d),t&&$(p)}}}function xt(t){let e,n,o,r,s,c,l,a,i,u,d,p,f,h,x,_,M,C,T,L,S,O,A,H,N,B,D=t[1].description+"",F=t[1].account+"",I=t[1].amount+"",j=t[1].category+"",z=ot(t[1].created_at)+"",q=t[1].images,J=[];for(let e=0;e<q.length;e+=1)J[e]=vt(bt(t,q,e));return{c(){e=y("h1"),n=v(D),o=w(),r=y("p"),s=y("b"),s.textContent="Account:",c=v(" "),l=v(F),a=w(),i=y("p"),u=y("b"),u.textContent="Amount:",d=v(" "),p=v(t[0]),f=w(),h=v(I),x=w(),_=y("p"),M=y("b"),M.textContent="Category:",C=v(" "),T=v(j),L=w(),S=y("p"),O=y("b"),O.textContent="Created at:",A=v(" "),H=v(z),N=w();for(let t=0;t<J.length;t+=1)J[t].c();B=v(""),k(e,"class","modal-title fs-5 mb-3"),k(e,"id","expense-modal-label")},m(t,$){g(t,e,$),m(e,n),g(t,o,$),g(t,r,$),m(r,s),m(r,c),m(r,l),g(t,a,$),g(t,i,$),m(i,u),m(i,d),m(i,p),m(i,f),m(i,h),g(t,x,$),g(t,_,$),m(_,M),m(_,C),m(_,T),g(t,L,$),g(t,S,$),m(S,O),m(S,A),m(S,H),g(t,N,$);for(let e=0;e<J.length;e+=1)J[e]&&J[e].m(t,$);g(t,B,$)},p(t,e){if(2&e&&D!==(D=t[1].description+"")&&E(n,D),2&e&&F!==(F=t[1].account+"")&&E(l,F),1&e&&E(p,t[0]),2&e&&I!==(I=t[1].amount+"")&&E(h,I),2&e&&j!==(j=t[1].category+"")&&E(T,j),2&e&&z!==(z=ot(t[1].created_at)+"")&&E(H,z),2&e){let n;for(q=t[1].images,n=0;n<q.length;n+=1){const o=bt(t,q,n);J[n]?J[n].p(o,e):(J[n]=vt(o),J[n].c(),J[n].m(B.parentNode,B))}for(;n<J.length;n+=1)J[n].d(1);J.length=q.length}},d(t){t&&$(e),t&&$(o),t&&$(r),t&&$(a),t&&$(i),t&&$(x),t&&$(_),t&&$(L),t&&$(S),t&&$(N),b(J,t),t&&$(B)}}}function vt(t){let e,n,o,r,s;return{c(){e=y("a"),n=y("img"),r=w(),k(n,"class","img-thumbnail mb-2"),l(n.src,o=t[3])||k(n,"src",o),k(n,"alt","Expenses attachment"),C(n,"object-fit","cover"),C(n,"width","100px"),C(n,"height","100px"),k(e,"href",s=t[3]),k(e,"target","_blank")},m(t,o){g(t,e,o),m(e,n),m(e,r)},p(t,r){2&r&&!l(n.src,o=t[3])&&k(n,"src",o),2&r&&s!==(s=t[3])&&k(e,"href",s)},d(t){t&&$(e)}}}function wt(e){let n,o,r,s,c,l,a,i,u,d,p,f;function h(t,e){return t[1].description?xt:yt}let b=h(e),x=b(e);return{c(){n=y("div"),o=y("div"),r=y("div"),s=y("div"),x.c(),c=w(),l=y("br"),a=w(),i=y("button"),i.textContent="Close",u=w(),d=y("a"),p=v("Update"),k(i,"type","button"),k(i,"class","text-end btn btn-secondary"),k(i,"data-bs-dismiss","modal"),k(d,"class","text-start btn btn-primary"),k(d,"href",f=e[1].url),k(s,"class","modal-body"),k(r,"class","modal-content"),k(o,"class","modal-dialog modal-dialog-centered"),k(n,"class","modal fade"),k(n,"id","expense-modal"),k(n,"tabindex","-1")},m(t,e){g(t,n,e),m(n,o),m(o,r),m(r,s),x.m(s,null),m(s,c),m(s,l),m(s,a),m(s,i),m(s,u),m(s,d),m(d,p)},p(t,[e]){b===(b=h(t))&&x?x.p(t,e):(x.d(1),x=b(t),x&&(x.c(),x.m(s,c))),2&e&&f!==(f=t[1].url)&&k(d,"href",f)},i:t,o:t,d(t){t&&$(n),x.d()}}}function _t(t,e,n){let{currency:o=""}=e,r={id:"",category:"",account:"",created_at:"",description:"",amount:0,action:""};var s;return s=nt.subscribe((t=>{if(Object.keys(r).forEach((t=>n(1,r[t]=null,r))),t){const e=new XMLHttpRequest;e.onreadystatechange=function(){e.readyState==XMLHttpRequest.DONE&&n(1,r=JSON.parse(e.responseText))},e.open("GET",`/expenses/detail/${t}`),e.send()}})),function(){if(!f)throw new Error("Function called outside component initialization");return f}().$$.on_destroy.push(s),t.$$set=t=>{"currency"in t&&n(0,o=t.currency)},[o,r]}const kt=class extends Y{constructor(t){super(),G(this,t,_t,wt,s,{currency:0})}};function Et(t){let e,n;return e=new ht({}),{c(){P(e.$$.fragment)},m(t,o){U(e,t,o),n=!0},i(t){n||(R(e.$$.fragment,t),n=!0)},o(t){W(e.$$.fragment,t),n=!1},d(t){X(e,t)}}}function Mt(t){let e,n,r,s,c,l,a,i,u,d,p;r=new $t({});let f=!t[1]&&Et();return i=new it({props:{currency:t[0]}}),d=new kt({props:{currency:t[0]}}),{c(){e=y("div"),n=y("div"),P(r.$$.fragment),s=w(),f&&f.c(),c=w(),l=y("hr"),a=w(),P(i.$$.fragment),u=w(),P(d.$$.fragment),k(n,"class","row pt-2 px-3"),k(e,"class","card")},m(t,o){g(t,e,o),m(e,n),U(r,n,null),m(n,s),f&&f.m(n,null),m(e,c),m(e,l),m(e,a),U(i,e,null),m(e,u),U(d,e,null),p=!0},p(t,[e]){t[1]?f&&(q={r:0,c:[],p:q},W(f,1,1,(()=>{f=null})),q.r||o(q.c),q=q.p):f?2&e&&R(f,1):(f=Et(),f.c(),R(f,1),f.m(n,null));const r={};1&e&&(r.currency=t[0]),i.$set(r);const s={};1&e&&(s.currency=t[0]),d.$set(s)},i(t){p||(R(r.$$.fragment,t),R(f),R(i.$$.fragment,t),R(d.$$.fragment,t),p=!0)},o(t){W(r.$$.fragment,t),W(f),W(i.$$.fragment,t),W(d.$$.fragment,t),p=!1},d(t){t&&$(e),X(r),f&&f.d(),X(i),X(d)}}}function Ct(t,e,n){let{currency:o="MYR"}=e,{hideFilter:r=!1}=e;return t.$$set=t=>{"currency"in t&&n(0,o=t.currency),"hideFilter"in t&&n(1,r=t.hideFilter)},[o,r]}const Tt=JSON.parse(document.getElementById("transaction-data").textContent)||[];V.set(Tt);const Lt=document.getElementById("user-currency").textContent,St=document.getElementById("hide-filter")&&"true"===document.getElementById("hide-filter").textContent;new class extends Y{constructor(t){super(),G(this,t,Ct,Mt,s,{currency:0,hideFilter:1})}}({target:document.getElementById("transactions"),props:{currency:Lt,hideFilter:St}})})();