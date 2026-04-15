export default defineNuxtRouteMiddleware((to) => {
  if (to.path !== "/registro") {
    useState("registro_form_data").value = defaultForm();
    useState("registro_form_errors").value = {};
    useState("registro_paso_actual").value = 1;
    useState("registro_loading").value = false;
    useState("registro_success").value = false;
  }
});
