package com.thesis.backend.config;

import com.thesis.backend.config.props.CorsProperties;
import com.thesis.backend.security.jwt.AuthEntryPointJwt;
import com.thesis.backend.security.jwt.AuthTokenFilter;
import com.thesis.backend.security.services.UserDetailsServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.autoconfigure.security.servlet.EndpointRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.builders.WebSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.Collections;

// – @EnableWebSecurity allows Spring to find and automatically apply the class to the global Web Security.
//
//– @EnableGlobalMethodSecurity provides AOP security on methods. It enables @PreAuthorize, @PostAuthorize,
// it also supports JSR-250. You can find more parameters in configuration in Method Security Expressions.
//
//– We override the configure(HttpSecurity http) method from WebSecurityConfigurerAdapter interface.
// It tells Spring Security how we configure CORS and CSRF,
// when we want to require all users to be authenticated or not, which filter (AuthTokenFilter)
// and when we want it to work (filter before UsernamePasswordAuthenticationFilter),
// which Exception Handler is chosen (AuthEntryPointJwt).
//
//– Spring Security will load User details to perform authentication & authorization.
// So it has UserDetailsService interface that we need to implement.
//
//– The implementation of UserDetailsService will be used for configuring
// DaoAuthenticationProvider by AuthenticationManagerBuilder.userDetailsService() method.
//
//– We also need a PasswordEncoder for the DaoAuthenticationProvider. If we don’t specify, it will use plain text.

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    UserDetailsServiceImpl userDetailsService;

    @Override
    public void configure(WebSecurity web) throws Exception {
        web.ignoring().antMatchers("/actuator/**");
    }

    @Autowired
    private AuthEntryPointJwt unauthorizedHandler;


    @Autowired
    private CorsProperties corsProperties;


    @Bean
    public AuthTokenFilter authTokenFilter() {
        return new AuthTokenFilter();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService).passwordEncoder(passwordEncoder());
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .cors().configurationSource(corsConfigurationSource()).and()
                .csrf().disable()
                .exceptionHandling().authenticationEntryPoint(unauthorizedHandler).and()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS).and()
                .authorizeRequests()
                .antMatchers("/api/auth/**").permitAll()
                .antMatchers("/api/init/**").permitAll()
                .antMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated();
        http.addFilterBefore(authTokenFilter(), UsernamePasswordAuthenticationFilter.class);
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        final CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList(corsProperties.getAllowOrigins()));
        configuration.setAllowCredentials(corsProperties.isAllowCredentials());
        configuration.setAllowedHeaders(Collections.singletonList("*"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

}
