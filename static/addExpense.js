(()=>{function e(e,n){document.getElementById(e).value=n}const n=new URLSearchParams(window.location.search),t=n.get("account");t&&e("id_from_account",t);const c=n.get("event");c&&e("id_event",c)})();
