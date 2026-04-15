import parsePhoneNumberFromString from "libphonenumber-js";

export const normalizePhone = (phone: string, country: any = "ES") => {
  if (!phone) return;

  const parsed = parsePhoneNumberFromString(phone, country);

  if (!parsed || !parsed.isValid()) return undefined;

  return parsed.format("E.164");
};

export const formatPhoneInput = (value: string) => {
  if (!value) return "+34 ";

  let digits = value.replace(/\D/g, "");

  if (digits.startsWith("34")) {
    digits = digits.slice(2);
  }

  digits = digits.slice(0, 9);

  const parts = digits.match(/.{1,3}/g) || [];
  return "+34 " + parts.join(" ");
};
