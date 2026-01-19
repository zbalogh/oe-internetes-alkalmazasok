// Oktatási modell: csak a szükséges mezőket vesszük fel.
// (A jsonplaceholder több mezőt is ad, de nem kell mind.)
export interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
}
