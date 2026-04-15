import { ZodError } from "zod";
import { AuthApiService } from "~/services/authApiService";
import type { Alergia } from "~/types/Alergia";
import type { RegistroForm } from "~/types/RegisterForm";

export const useRegistroForm = () => {
  const pasoActual = useState("registro_paso_actual", () => 1);
  const totalPasos = 3;

  const serverMessage = useState("server_message", () => "");
  const serverProgress = useState("server_progress", () => 0);

  const isSubmitting = useState("registro_loading", () => false);
  const isSuccess = useState("registro_success", () => false);

  const errors = useState<Record<string, string>>(
    "registro_form_errors",
    () => ({}),
  );

  const form = useState<RegistroForm>("registro_form_data", () => ({
    nombre: "",
    apellidos: "",
    fecha_nacimiento: "",
    ciudad: "",
    alergias: [],
    medicacion: "",
    email: "",
    telefono: "",
    password: "",
    password_confirmation: "",
    acepta_notificaciones: false,
    como_nos_conocio: "",
  }));

  const clearError = (path: string) => {
    delete errors.value[path];
  };

  const validarPaso = () => {
    errors.value = {};
    try {
      if (pasoActual.value === 1) {
        paso1Schema.parse(form.value);
      } else if (pasoActual.value === 2) {
        paso2Schema.parse(form.value);
      }
      return true;
    } catch (error) {
      if (error instanceof ZodError) {
        error.issues.forEach((issue) => {
          const field = issue.path[0] as keyof typeof errors.value;
          errors.value[field] = issue.message;
          console.error(issue);
        });
        console.log(errors.value);
      } else {
        console.error("Error inesperado:", error);
      }
      return false;
    }
  };

  const siguientePaso = () => {
    if (validarPaso() && pasoActual.value < totalPasos) pasoActual.value++;
  };

  const pasoAnterior = () => {
    if (pasoActual.value > 1) pasoActual.value--;
  };

  const toggleAlergia = (alergia: Alergia["nombre"]) => {
    const index = form.value.alergias.findIndex((a) => a.nombre === alergia);

    if (index === -1) {
      form.value.alergias.push({ nombre: alergia, severidad: "leve" });
    } else {
      form.value.alergias.splice(index, 1);
    }
  };

  const setSeveridad = (nombre: string, severidad: Alergia["severidad"]) => {
    form.value.alergias = form.value.alergias.map((a) =>
      a.nombre === nombre ? { ...a, severidad } : a,
    );
  };

  const submit = async () => {
    if (isSubmitting.value) return;

    isSubmitting.value = true;

    try {
      registroTotalSchema.parse(form.value);
      const payload = {
        ...form.value,
        telefono: normalizePhone(form.value.telefono),
      };

      errors.value = {};
      await AuthApiService.register(payload, (payload) => {
        serverMessage.value = payload.message;
        serverProgress.value = payload.progress;
        if (payload.done) {
          setTimeout(() => {
            isSuccess.value = true;
            isSubmitting.value = false;
          }, 1000);
        }
      });
      isSuccess.value = true;
    } catch (error: any) {
      isSubmitting.value = false;
      if (error instanceof ZodError) {
        error.issues.forEach((issue) => {
          const field = issue.path[0] as keyof typeof errors.value;
          errors.value[field] = issue.message;
        });
      } else if (error.data) {
        const serverErrors = error.data;

        Object.keys(serverErrors).forEach((key) => {
          const mensaje = Array.isArray(serverErrors[key])
            ? serverErrors[key][0]
            : serverErrors[key];

          errors.value[key] = mensaje;
          console.error(`Error en campo ${key}:`, mensaje);
        });
      } else {
        console.error("Error inesperado:", error);
        errors.value.general =
          error.message ||
          "Ha ocurrido un error inesperado. Inténtalo de nuevo.";
      }
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    isSubmitting,
    serverMessage,
    serverProgress,
    isSuccess,
    form,
    pasoActual,
    totalPasos,
    errors,
    clearError,
    siguientePaso,
    pasoAnterior,
    toggleAlergia,
    setSeveridad,
    submit,
  };
};
