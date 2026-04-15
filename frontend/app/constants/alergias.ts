export const ALERGENOS = [
  "Gramíneas",
  "Olivo",
  "Abedul",
  "Artemisa",
  "Ambrosía",
  "Aliso",
  "Ácaros",
  "Pelo de gato",
  "Pelo de perro",
] as const;

export const SEVERIDADES = [
  { label: "Leve", value: "leve" },
  { label: "Moderada", value: "moderada" },
  { label: "Severa", value: "severa" },
] as const;

export type AlergiaNombre = (typeof ALERGENOS)[number];
export type SeveridadValue = (typeof SEVERIDADES)[number]["value"];
