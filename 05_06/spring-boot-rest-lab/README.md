# Spring Boot REST Lab (MVC + REST alapok)

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

## Swagger UI
- http://localhost:8080/swagger-ui.html

## API végpontok
- GET    http://localhost:8080/api/v1/users
- GET    http://localhost:8080/api/v1/users/{id}
- POST   http://localhost:8080/api/v1/users
- PUT    http://localhost:8080/api/v1/users/{id}
- DELETE http://localhost:8080/api/v1/users/{id}

## Gyors teszt curl-lel
```bash
curl -s http://localhost:8080/api/v1/users | jq

curl -i -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Charlie","email":"charlie@example.com"}'

curl -i -X DELETE http://localhost:8080/api/v1/users/1
```
