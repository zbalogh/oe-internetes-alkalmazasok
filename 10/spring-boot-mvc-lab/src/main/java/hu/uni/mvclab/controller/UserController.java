package hu.uni.mvclab.controller;

import hu.uni.mvclab.dto.User;
import hu.uni.mvclab.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * Classic MVC Controller for User CRUD operations
 * Handles HTTP requests and returns view names (HTML templates)
 */
@Controller
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * Show all users - List page
     * GET /users
     */
    @GetMapping
    public String listUsers(Model model)
    {
        model.addAttribute("users", userService.getAllUsers());
        return "user-list"; // returns user-list.html template
    }

    /**
     * Show form to create a new user
     * GET /users/new
     */
    @GetMapping("/new")
    public String showCreateForm(Model model)
    {
        model.addAttribute("user", new User());
        return "user-form"; // returns user-form.html template
    }

    /**
     * Process the creation of a new user
     * POST /users
     */
    @PostMapping
    public String createUser(@ModelAttribute("user") User user, RedirectAttributes redirectAttributes)
    {
        userService.createUser(user);
        redirectAttributes.addFlashAttribute("message", "User created successfully!");
        return "redirect:/users"; // redirect to list page
    }

    /**
     * Show form to edit an existing user
     * GET /users/edit/{id}
     */
    @GetMapping("/edit/{id}")
    public String showEditForm(@PathVariable Long id, Model model)
    {
        User user = userService.getUserById(id);

        if (user == null) {
            return "redirect:/users";
        }

        model.addAttribute("user", user);
        return "user-form"; // returns user-form.html template
    }

    /**
     * Process the update of an existing user
     * POST /users/update/{id}
     */
    @PostMapping("/update/{id}")
    public String updateUser(@PathVariable Long id,
                             @ModelAttribute("user") User user,
                             RedirectAttributes redirectAttributes)
    {
        User updatedUser = userService.updateUser(id, user);

        if (updatedUser != null) {
            redirectAttributes.addFlashAttribute("message", "User updated successfully!");
        } else {
            redirectAttributes.addFlashAttribute("error", "User not found!");
        }

        return "redirect:/users"; // redirect to list page
    }

    /**
     * Delete a user
     * GET /users/delete/{id}
     */
    @GetMapping("/delete/{id}")
    public String deleteUser(@PathVariable Long id, RedirectAttributes redirectAttributes)
    {
        boolean deleted = userService.deleteUser(id);

        if (deleted) {
            redirectAttributes.addFlashAttribute("message", "User deleted successfully!");
        } else {
            redirectAttributes.addFlashAttribute("error", "User not found!");
        }

        return "redirect:/users"; // redirect to list page
    }

}
