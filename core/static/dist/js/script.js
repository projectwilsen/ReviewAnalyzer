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
// const pwShowHide = document.querySelectorAll("#pw_hide");
// console.log(pwShowHide)

// pwShowHide.forEach(icon =>{
//     icon.addEventListener("click", () =>{
//         let getPwInput = icon.parentElement.querySelector("input");
//         if(getPwInput.type === "password"){
//             getPwInput.type = "text";
//             icon.classList.replace("uil-eye-slash","uil-eye");
//         }else{
//             getPwInput.type = "password";
//             icon.classList.replace("uil-eye","uil-eye-slash");
//         }
//     });
// });


// function updateChatBot(chatbot_info){
  // const elementsToReplace = document.querySelectorAll('.replace');
  // let replacementContent = [chatbot_info.videoid, chatbot_info.videotitle,
  //                           chatbot_info.view, chatbot_info.like, chatbot_info.comment]


  // elementsToReplace.forEach(function(element, index) {
  //   var newElement = document.createElement('span');
  //   newElement.textContent = replacementContent[index];

  //   element.parentNode.replaceChild(newElement, element);
  // });
// }

// function showHistory(h) {

//   const djangoDate = new Date(h.last_update);
//   const currentDate = new Date();
  
//   const timeDiff = currentDate.getTime() - djangoDate.getTime();
  
//   const secondsDiff = Math.floor(timeDiff / 1000);

//   // Calculate the elapsed days, hours, minutes, and seconds
//   const days = Math.floor(secondsDiff / (24 * 60 * 60));
//   const hours = Math.floor((secondsDiff % (24 * 60 * 60)) / (60 * 60));
//   const minutes = Math.floor((secondsDiff % (60 * 60)) / 60);
//   const seconds = Math.floor(secondsDiff % 60);

//   return `<button id = "history_button" data-id = ${h.id} class="group text-left w-[380px] h-[100px] relative bg-white/10 p-5 rounded-lg backdrop-filter backdrop-blur-xl shadow-lg hover:bg-white transition duration-300 ease-in-out focus:bg-white">

//             <h1 class="pr-5 font-nunito font-bold text-sm text-slate-100 group-hover:bg-gradient-to-b group-hover:from-red-600 group-hover:to-red-950 group-hover:bg-clip-text group-hover:text-transparent group-focus:bg-gradient-to-b group-focus:from-red-600 group-focus:to-red-950 group-focus:bg-clip-text group-focus:text-transparent">
//               ${h.videotitle}
//             </h1>
         
//             <h1 class="font-nunito text-sm text-slate-400 mt-1 group-hover:text-black group-focus:text-black ">
//               ${getTimeAgo(days, hours, minutes, seconds)}
//             </h1>

//             <a href="" class=" close font-nunito absolute pr-4 pt-1 text-slate-600 top-0 right-0 group-hover:text-black group-focus:text-black">
//               x
//             </a>
//           </button>`;
// }

// function getTimeAgo(days, hours, minutes, seconds) {
//   if (days > 0) {
//     return `${days} days ago`;
//   } else if (hours > 0) {
//     return `${hours} hours ago`;
//   } else if (minutes > 0) {
//     return `${minutes} minutes ago`;
//   } else {
//     return `${seconds} seconds ago`;
//   }
// }

// function storeFocusedElement() {

//   const focusedElement = document.activeElement;
//   console.log(focusedElement)
//   if (focusedElement) {
//     const focusedElementDataId = focusedElement.getAttribute('data-id');
//     localStorage.setItem('focusedElementDataId', focusedElementDataId);
//   }
// }

// function storeFocusedElement(id = null) {

//   if (id === null){
//     const focusedElement = document.activeElement;
//     console.log(focusedElement)
//     if (focusedElement) {
//       const focusedElementDataId = focusedElement.getAttribute('data-id');
//       localStorage.setItem('focusedElementDataId', focusedElementDataId);
//     }
//   } else {
//     localStorage.setItem('focusedElementDataId', id)
//   }
// }

// function restoreFocus() {
//   const focusedElementDataId = localStorage.getItem('focusedElementDataId');
//   if (focusedElementDataId) {
//     const focusedElement = document.querySelector(`[data-id="${focusedElementDataId}"]`);
//     console.log(focusedElement)
//     if (focusedElement) {
//       focusedElement.focus();
//     }
//   }
// }

