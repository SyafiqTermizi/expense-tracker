(()=>{"use strict";const e=document.getElementById("imageInput"),t=document.getElementById("imagePreview"),n=document.getElementById("imageLink"),s=document.getElementById("imageContainer"),c=document.getElementById("imageRemoveButton");let o=null;t.classList.contains("d-none")||(o=t.src),e.onchange=o=>{const[i]=e.files;i&&(t.classList.remove("d-none"),t.src=URL.createObjectURL(i),n.href=URL.createObjectURL(i),s.classList.add("input-group"),c.classList.remove("d-none"))},c.onclick=i=>{o?(t.src=o,n.href=o):(t.classList.add("d-none"),t.src="",n.href="#"),s.classList.remove("input-group"),c.classList.add("d-none"),e.files=null,e.value=""}})();