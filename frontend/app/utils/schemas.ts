import { z } from "zod";
import { ALERGENOS, SEVERIDADES } from "~/constants/alergias";
import { CIUDADES_LABELS, CIUDADES_VALUES } from "~/constants/ciudades";

// Register Form
// Esquema Paso 1
export const paso1Schema = z.object({
  nombre: z.string().min(2, "El nombre es demasiado corto"),
  apellidos: z.string().min(2, "Los apellidos son obligatorios"),
  fecha_nacimiento: z
    .string()
    .min(1, "La fecha es obligatoria")
    .refine(
      (data) => {
        const birth = new Date(data);
        const today = new Date();

        const age = today.getFullYear() - birth.getFullYear();

        return age >= 0 && age <= 120;
      },
      {
        message: "Fecha de nacimiento inválida",
      },
    ),
  ciudad: z.enum(CIUDADES_VALUES),
});

// Esquema Paso 2
export const paso2Schema = z.object({
  alergias: z
    .array(
      z.object({
        nombre: z.enum(ALERGENOS),
        severidad: z.enum(SEVERIDADES.map((severidad) => severidad.value)),
      }),
    )
    .min(1, "Selecciona al menos una alergia"),
  medicacion: z.string().optional(),
});

// Esquema Paso 3
export const paso3Schema = z
  .object({
    email: z.string().email("Email inválido"),
    telefono: z
      .string()
      .transform((v) => v?.trim())
      .optional()
      .refine((v) => {
        if (!v) return true;
        return v.replace(/\D/g, "").length === 11;
      }, "Teléfono inválido"),
    password: z.string().min(8, "Mínimo 8 caracteres"),
    password_confirmation: z.string(),
    acepta_notificaciones: z.boolean().optional(),
    como_nos_conocio: z.string().min(1, "Selecciona una opción"),
  })
  .refine((data) => data.password === data.password_confirmation, {
    message: "Las contraseñas no coinciden",
    path: ["password_confirmation"],
  });

// Esquema Completo (para el servidor)
export const registroTotalSchema = z.intersection(
  z.intersection(paso1Schema, paso2Schema),
  paso3Schema,
);
