export const defaultForm = () => ({
  nombre: "",
  apellidos: "",
  fecha_nacimiento: "",
  ciudad: "",
  alergias: [] as { nombre: string; severidad: string }[],
  medicacion: "",
  email: "",
  telefono: "",
  password: "",
  password_confirmation: "",
  acepta_notificaciones: false,
  como_nos_conocio: "",
});

export type RegistroForm = ReturnType<typeof defaultForm>;
