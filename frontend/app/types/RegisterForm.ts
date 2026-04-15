import type { Alergia } from "./Alergia";
import type { Ciudad } from "./Ciudad";

export type RegistroForm = {
  nombre: string;
  apellidos: string;
  fecha_nacimiento: string;
  ciudad: string;
  // Paso 2
  alergias: Alergia[];
  medicacion: string;

  // Paso 3
  email: string;
  telefono: string;
  password: string;
  password_confirmation: string;
  acepta_notificaciones: boolean;
  como_nos_conocio: "instagram" | "tiktok" | "amigos_otros" | "";
};

export type RegistroOutput = Omit<RegistroForm, "password_confirmation">;
