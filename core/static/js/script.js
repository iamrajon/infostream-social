//  // Add click event listener to each button
//  const buttons = document.querySelectorAll('.btn-hover');
//  buttons.forEach(button => {
//    button.addEventListener('click', () => {
//      // Remove underline from all buttons
//      buttons.forEach(btn => btn.classList.remove('btn-clicked'));
//      // Add underline to the clicked button
//      button.classList.add('btn-clicked');
//    });
//  });


const buttons = document.querySelectorAll('.btn-toggle');
buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Toggle active class on button
    button.classList.toggle('active');
  });
});