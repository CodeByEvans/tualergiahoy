import type { FieldConfig } from "~/types/Forms";
import { CIUDADES } from "./ciudades";

const hoy = new Date().toISOString().split("T")[0];

export const PERSONAL_FIELDS: FieldConfig[] = [
  {
    name: "nombre",
    label: "Nombre",
    required: true,
    placeholder: "Tu nombre",
  },
  {
    name: "apellidos",
    label: "Apellidos",
    required: true,
    placeholder: "Tus apellidos",
  },
  {
    name: "fecha_nacimiento",
    label: "Fecha de nacimiento",
    required: true,
    type: "date",
    max: hoy,
    placeholder: "Tu fecha de nacimiento",
  },
  {
    name: "ciudad",
    label: "Provincia",
    inputType: "menu",
    items: CIUDADES,
    icon: "i-heroicons-map-pin",
  },
];

export const ACCOUNT_FIELDS: FieldConfig[] = [
  {
    name: "email",
    label: "Correo electrónico",
    type: "email",
    required: true,
    placeholder: "email@dominio.com",
  },
  {
    name: "telefono",
    label: "Teléfono",
    type: "tel",
    inputType: "phone",
    maxlength: 15,
    placeholder: "+34 xxx xxx xxx",
  },
  {
    name: "password",
    label: "Contraseña",
    type: "password",
    required: true,
    placeholder: "Tu contraseña",
    isPassword: true, // Flag para activar el ojo en la molécula
  },
  {
    name: "password_confirmation",
    label: "Confirmar contraseña",
    type: "password",
    required: true,
    placeholder: "Confirma tu contraseña",
    isPassword: true,
  },
  {
    name: "acepta_notificaciones",
    label: "¿Quieres recibir notificaciones?",
    inputType: "switch",
  },
  {
    name: "como_nos_conocio",
    label: "¿Cómo nos conociste?",
    inputType: "select",
    required: true,
    placeholder: "Selecciona una opción",
    items: [
      { label: "Instagram", value: "instagram" },
      { label: "TikTok", value: "tiktok" },
      { label: "Amigos / Otros", value: "amigos_otros" },
    ],
  },
];

export const STEPS_CONFIG = {
  PERSONAL: {
    title: "Datos personales",
    description: "Cuéntanos un poco sobre ti para empezar",
    fields: PERSONAL_FIELDS,
  },
  ACCOUNT: {
    title: "Configuración de cuenta",
    description: "Seguridad y preferencias de contacto",
    fields: ACCOUNT_FIELDS,
  },
};
