# Spring Boot MVC Demo alkalmazás

## Előfeltételek
- JDK 17 vagy 21
- Maven 3.9+
- IDE: IntelliJ IDEA / Eclipse / VS Code
- VS Code-ban ajánlott telepíteni az "Extension Pack for Java" extension-t

## Compile & Build
```bash
mvnw clean package
```

## Futtatás
```bash
mvnw spring-boot:run
```

## A projekt struktúrája

A projekt egy **klasszikus MVC (Model-View-Controller)** architektúrát követ:

```
src/main/java/hu/uni/mvclab/
├── SpringBootMvcLabApplication.java  (Főprogram)
├── controller/
│   ├── HomeController.java           (Root URL átirányítása)
│   └── UserController.java           (MVC Controller - CRUD műveletek)
├── dto/
│   └── User.java                     (Data Transfer Object - Model)
└── service/
    └── UserService.java              (Service réteg - üzleti logika)

src/main/resources/
├── application.properties            (Konfiguráció)
└── templates/                        (Thymeleaf HTML sablonok)
    ├── user-list.html                (Felhasználók listázása)
    └── user-form.html                (Létrehozás/szerkesztés űrlap)
```

#### Controller műveletek:
- `GET /users` → `listUsers()` → "user-list" view
- `GET /users/new` → `showCreateForm()` → "user-form" view
- `POST /users` → `createUser()` → redirect:/users
- `GET /users/edit/{id}` → `showEditForm()` → "user-form" view
- `POST /users/update/{id}` → `updateUser()` → redirect:/users
- `GET /users/delete/{id}` → `deleteUser()` → redirect:/users


### Használat:
Nyisd meg a böngészőt: `http://localhost:8080`

- Automatikusan átirányít a `/login` oldalra
- Jelentkezz be az `admin` felhasználóval, jelszó: `admin123`
- A bejelentkezés után átirányít a `/users` oldalra
- Lista nézetben láthatóak a felhasználók
- "Add New User" gomb - új felhasználó létrehozása
- "Edit" gomb - felhasználó szerkesztése
- "Delete" gomb - felhasználó törlése (megerősítéssel)
- "Refresh List" gomb - lista frissítése
- "Logout" gomb - kijelentkezés


## Tanulási célok - mit demonstrál ez az alkalmazás?

1. **MVC Architektúra**
   - Szétválasztott rétegek (Model, View, Controller)
   - Service réteg az üzleti logikának
   

2. **Spring Boot MVC**
   - `@Controller` használata
   - `@GetMapping`, `@PostMapping` annotációk
   - `Model` objektum használata
   - `@ModelAttribute` - form binding
   - `@PathVariable` - URL paraméterek
   - `RedirectAttributes` - flash üzenetek


3. **Spring Security Alapok**
   - Form alapú autentikáció
   - In-memory user store
   - Login és logout kezelése


4. **Thymeleaf Template Engine**
   - Szerver oldali HTML renderelés
   - Thymeleaf attribútumok (`th:*`)
   - Feltételes renderelés (`th:if`)
   - Iteráció (`th:each`)
   - Form binding (`th:field`)
   - URL generálás (`@{...}`)


5. **CRUD műveletek**
   - Create (POST /users)
   - Read (GET /users, GET /users/edit/{id})
   - Update (POST /users/update/{id})
   - Delete (GET /users/delete/{id})
