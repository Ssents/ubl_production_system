const showMenuBar = (toggleID, navbarID, mainBodyID)=>{
    const toggle = document.getElementById(toggleID);
    const navBar = document.getElementById(navbarID);
    const mainBody = document.getElementById(mainBodyID);

    if (toggle && navBar){
        toggle.addEventListener('click', ()=>{
            navBar.classList.toggle('show');
            mainBody.classList.toggle('show');
        });
    }
};

showMenuBar('sidebar-toggler-id', 'side-nav', 'body-toggle');
