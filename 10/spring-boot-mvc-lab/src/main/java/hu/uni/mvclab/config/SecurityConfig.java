package hu.uni.mvclab.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Spring Security configuration class
 *
 * This class is responsible for security settings:
 * - All pages are protected (authentication required)
 * - Form-based login is used
 * - In-memory user storage
 * - Logout functionality
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /**
     * SecurityFilterChain - configure security filters
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception
    {
        http
                // Endpoint authorization settings
                .authorizeHttpRequests(authorize -> authorize
                        // CSS and static files are publicly accessible (optional)
                        .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
                        // All other URLs require authentication
                        .anyRequest().authenticated()
                )
                // Enable form-based login
                // Use Spring Security default login page
                .formLogin(form -> form
                        .permitAll()  // Login page accessible to everyone
                )
                // Enable logout
                .logout(logout -> logout
                        .logoutUrl("/logout")           // Logout URL
                        .logoutSuccessUrl("/login")     // Redirect to login page after successful logout
                        .permitAll()                    // Logout accessible to everyone
                );

        return http.build();
    }

    /**
     * PasswordEncoder Bean - password encryption/hashing
     *
     * Uses BCrypt algorithm - secure and industry standard
     */
    @Bean
    public PasswordEncoder passwordEncoder()
    {
        return new BCryptPasswordEncoder();
    }

    /**
     * UserDetailsService Bean - user management
     *
     * In-memory storage with a single "dummy" user
     * No database required - ideal for educational purposes
     */
    @Bean
    public UserDetailsService userDetailsService()
    {
        // Create user
        UserDetails user = User.builder()
                .username("admin")  // Username
                .password(passwordEncoder().encode("admin123")) // Password (BCrypt hashed)
                .roles("ADMIN")
                .build();

        // In-memory storage - with a single user
        return new InMemoryUserDetailsManager(user);
    }

}
