function attachHooks () {
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

  // const collapseElementList = document.querySelectorAll('.collapse');
  // console.log(collapseElementList)
  // const collapseList = [...collapseElementList].map(collapseEl => bootstrap.Collapse.getOrCreateInstance(collapseEl));
  // console.log(collapseList)

}

window.onload = () => {
  // wait till cbuttons are drawn and hook bootstrap popover listeners
  const interval = setInterval(() => {
    const cbuttons = document.getElementsByClassName('cbutton');

    if (cbuttons.length > 0) {
      clearInterval(interval);

      for (let cbutton of cbuttons) {
        cbutton.addEventListener('click', (e) => {
          e.target.classList.toggle('clicked');
        });
      }
      // on tab change, find popover elements and create bootstrap hooks
      [...document.querySelectorAll('.tab')].forEach((tab) => {
        tab.addEventListener('click', () => {
          attachHooks();
        });
      });

      // ... and initialise for the current tab
      attachHooks();

    }
  }, 100); // check every 100ms
};
