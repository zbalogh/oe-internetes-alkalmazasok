package hu.uni.mvclab.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Home controller - redirects root URL to user list
 */
@Controller
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "redirect:/users";
    }

}

