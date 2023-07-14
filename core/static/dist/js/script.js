// Navbar Fixed
window.onscroll = function () {
    const header = document.querySelector('header');
    const fixedNav = header.offsetTop;
    const toTop = document.querySelector('#to-top');
  
    if (window.pageYOffset > fixedNav) {
      header.classList.add('navbar-fixed');
    } else {
      header.classList.remove('navbar-fixed');
    }
  };

// Hamburger
const hamburger = document.querySelector('#hamburger');
const navMenu = document.querySelector('#nav-menu');

hamburger.addEventListener('click', function () {
  hamburger.classList.toggle('hamburger-active');
  navMenu.classList.toggle('hidden');
});

// Klik di luar hamburger
window.addEventListener('click', function (e) {
    if (e.target != hamburger && e.target != navMenu) {
      hamburger.classList.remove('hamburger-active');
      navMenu.classList.add('hidden');
    }
  });



// Darkmode toggle
const darkToggle = document.querySelector('#dark-toggle');
const html = document.querySelector('html');

darkToggle.addEventListener('click', function () {
  if (darkToggle.checked) {
    html.classList.add('dark');
    localStorage.theme = 'dark';
  } else {
    html.classList.remove('dark');
    localStorage.theme = 'light';
  }
});

// pindahkan posisi toggle sesuai mode
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  darkToggle.checked = true;
} else {
  darkToggle.checked = false;
}

// hidden pass
const pwShowHide = document.querySelectorAll("#pw_hide");

pwShowHide.forEach(icon =>{
    icon.addEventListener("click", () =>{
        let getPwInput = icon.parentElement.querySelector("input");
        if(getPwInput.type === "password"){
            getPwInput.type = "text";
            icon.classList.replace("uil-eye-slash","uil-eye");
        }else{
            getPwInput.type = "password";
            icon.classList.replace("uil-eye","uil-eye-slash");
        }
    });
});

// //chatbot
// document.getElementById('chatbot').scrollIntoView({
//   behavior: 'smooth',
//   block: 'end',
//   inline: 'nearest',
// });


// function showHistory(m) {
//   return `div class = " group w-[380px] h-[100px] relative bg-white/10 p-5 rounded-lg backdrop-filter backdrop-blur-xl shadow-lg hover:bg-white transition duration-300 ease-in-out">
//             <h1 class = "font-nunito font-bold text-sm text-slate-100 group-hover:bg-gradient-to-b group-hover:from-red-600 group-hover:to-red-950 group-hover:bg-clip-text group-hover:text-transparent group-hover:text-white">
//               ${m.title}
//             </h1>
//             <h1 class = "font-nunito text-sm text-slate-400 mt-1 group-hover:text-black group-focus:text-black">
//               ${m.created_at}
//             </h1>
//           </div>`
// }