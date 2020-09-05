/*https://bootstrapious.com/p/bootstrap-vertical-navbar*/
 // Sidebar toggle behavior function
$(function() {
  // Sidebar toggle behavior
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
});