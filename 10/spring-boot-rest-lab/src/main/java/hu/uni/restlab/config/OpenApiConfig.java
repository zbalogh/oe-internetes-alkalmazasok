package hu.uni.restlab.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OpenAPI/Swagger configuration for JWT authentication.
 *
 * This class configures Swagger UI to support Bearer token authentication,
 * allowing users to test protected endpoints directly from the Swagger interface.
 */
@Configuration
public class OpenApiConfig {

    private static final String SECURITY_SCHEME_NAME = "Bearer Authentication";

    /**
     * Configure OpenAPI with JWT Bearer authentication support.
     *
     * This adds an "Authorize" button to Swagger UI where users can input their JWT token.
     */
    @Bean
    public OpenAPI customOpenAPI()
    {
        return new OpenAPI()
                .info(new Info()
                        .title("REST Lab API with JWT Security")
                        .version("1.0.0")
                        .description("Spring Boot REST API Demo with JWT Authentication\n\n" +
                                "**How to use:**\n" +
                                "1. Call `/api/v1/auth/login` with the demo credentials\n" +
                                "2. Copy the token from the response\n" +
                                "3. Click the **Authorize** button (🔓) at the top\n" +
                                "4. Enter: `<your_token>`\n" +
                                "5. Click **Authorize** and close the dialog\n" +
                                "6. Now you can test all protected endpoints!"))
                .addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_NAME))
                .components(new Components()
                        .addSecuritySchemes(SECURITY_SCHEME_NAME,
                                new SecurityScheme()
                                        .name(SECURITY_SCHEME_NAME)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Enter JWT token obtained from /api/v1/auth/login endpoint")));
    }

}
