import cv2
import mediapipe as mp
import pyautogui
import time
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class HandySlidesConfig:
    def __init__(self):
        self.config_file = "handyslides_config.json"
        self.settings = self.load_config()
        
    def load_config(self):
        """Load saved settings or use defaults"""
        default_settings = {
            "right_arm_action": "next",  # "next" or "previous"
            "left_arm_action": "previous",
            "sensitivity": 0.05,
            "cooldown": 1.0,
            "show_debug": True,
            "powerpoint_keys": True,  # True for arrows, False for Page Up/Down
            "language": "en",  # "pt" for Portuguese, "en" for English, "fr" for French
            "mirror_camera": False # True to mirror camera feed
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
            except:
                pass
        
        return default_settings
    
    def save_config(self):
        """Save current settings"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

# Translation dictionary
TRANSLATIONS = {
    "pt": {
        "title": "HandySlides - Configuração",
        "gesture_config": "Configuração de Gestos",
        "right_arm": "Braço Direito:",
        "left_arm": "Braço Esquerdo:",
        "next": "Próximo",
        "previous": "Anterior",
        "advanced_config": "Configurações Avançadas",
        "sensitivity": "Sensibilidade:",
        "cooldown": "Cooldown (seg):",
        "options": "Opções",
        "show_debug": "Mostrar informações de debug",
        "use_arrows": "Usar setas do teclado (desmarque para Page Up/Down)",
        "mirror_camera": "Espelhar imagem da câmara",
        "language": "Idioma:",
        "test_camera": "Testar Câmara",
        "restore_defaults": "Restaurar Padrões",
        "save_config": "Guardar Configuração",
        "cancel": "Cancelar",
        "start": "Iniciar",
        "camera_error": "Câmara não detectada ou não está a funcionar!",
        "camera_success": "Câmara está a funcionar corretamente!",
        "invalid_config": "Configuração Inválida",
        "same_function": "Os dois braços não podem ter a mesma função!",
        "config_saved": "Configuração Guardada",
        "config_saved_msg": "Configurações guardadas com sucesso!",
        "error": "Erro",
        "success": "Sucesso",
        "info": "Informação"
    },
    "en": {
        "title": "HandySlides - Configuration",
        "gesture_config": "Gesture Configuration",
        "right_arm": "Right Arm:",
        "left_arm": "Left Arm:",
        "next": "Next",
        "previous": "Previous",
        "advanced_config": "Advanced Settings",
        "sensitivity": "Sensitivity:",
        "cooldown": "Cooldown (sec):",
        "options": "Options",
        "show_debug": "Show debug information",
        "use_arrows": "Use keyboard arrows (uncheck for Page Up/Down)",
        "mirror_camera": "Mirror camera image",
        "language": "Language:",
        "test_camera": "Test Camera",
        "restore_defaults": "Restore Defaults",
        "save_config": "Save Configuration",
        "cancel": "Cancel",
        "start": "Start",
        "camera_error": "Camera not found or not working!",
        "camera_success": "Camera is working correctly!",
        "invalid_config": "Invalid Configuration",
        "same_function": "Both arms cannot have the same function!",
        "config_saved": "Configuration Saved",
        "config_saved_msg": "Settings saved successfully!",
        "error": "Error",
        "success": "Success",
        "info": "Information"
    },
    "fr": {
        "title": "HandySlides - Configuration",
        "gesture_config": "Configuration des gestes",
        "right_arm": "Bras droit :",
        "left_arm": "Bras gauche :",
        "next": "Suivant",
        "previous": "Précédent",
        "advanced_config": "Paramètres avancés",
        "sensitivity": "Sensibilité :",
        "cooldown": "Refroidissement (sec) :",
        "options": "Options",
        "show_debug": "Afficher les informations de débogage",
        "use_arrows": "Utiliser les flèches du clavier (décocher pour Page Haut/Bas)",
        "mirror_camera": "Miroir de l'image de la caméra",
        "language": "Langue :",
        "test_camera": "Tester la caméra",
        "restore_defaults": "Restaurer les valeurs par défaut",
        "save_config": "Enregistrer la configuration",
        "cancel": "Annuler",
        "start": "Démarrer",
        "camera_error": "Caméra non trouvée ou non fonctionnelle !",
        "camera_success": "La caméra fonctionne correctement !",
        "invalid_config": "Configuration invalide",
        "same_function": "Les deux bras ne peuvent pas avoir la même fonction !",
        "config_saved": "Configuration enregistrée",
        "config_saved_msg": "Paramètres enregistrés avec succès !",
        "error": "Erreur",
        "success": "Succès",
        "info": "Information"
    }
}

class ConfigWindow:
    def __init__(self):
        self.config = HandySlidesConfig()
        self.root = tk.Tk()
        
        # Set initial language
        self.current_language = self.config.settings.get("language", "en")
        self.texts = TRANSLATIONS[self.current_language]
        
        self.root.title(self.texts["title"])
        self.root.resizable(True, True)
        
        # Center window after creating widgets
        self.root.after(100, self.center_window)
        
        # Variables
        self.sensitivity_var = tk.DoubleVar(value=self.config.settings["sensitivity"])
        self.cooldown_var = tk.DoubleVar(value=self.config.settings["cooldown"])
        self.debug_var = tk.BooleanVar(value=self.config.settings["show_debug"])
        self.keys_var = tk.BooleanVar(value=self.config.settings["powerpoint_keys"])
        self.language_var = tk.StringVar(value=self.current_language)
        self.mirror_var = tk.BooleanVar(value=self.config.settings["mirror_camera"])
        
        # Convert arm values to translated text
        right_action = self.config.settings["right_arm_action"]
        left_action = self.config.settings["left_arm_action"]
        
        self.right_arm_var = tk.StringVar(value=self.texts["next"] if right_action == "next" else self.texts["previous"])
        self.left_arm_var = tk.StringVar(value=self.texts["next"] if left_action == "next" else self.texts["previous"])
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text=self.texts["title"], 
                              font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Language selection (top)
        language_frame = ttk.LabelFrame(main_frame, text=self.texts["language"], padding=10)
        language_frame.pack(fill="x", pady=5)
        
        # Mapping to full language names
        language_options = {
            "English": "en",
            "Français": "fr",
            "Português": "pt"
        }
        
        # Find the full name of current language
        language_name_map = {"en": "English", "fr": "Français", "pt": "Português"}
        current_language_name = language_name_map.get(self.current_language, "English")
        self.language_display_var = tk.StringVar(value=current_language_name)
        
        language_combo = ttk.Combobox(language_frame, textvariable=self.language_display_var, 
                                     values=list(language_options.keys()), state="readonly", width=20)
        language_combo.pack(anchor="w")
        language_combo.bind("<<ComboboxSelected>>", lambda e: self.change_language_by_name(language_options))
        
        # Arm gesture configuration
        self.gesture_frame = ttk.LabelFrame(main_frame, text=self.texts["gesture_config"], padding=10)
        self.gesture_frame.pack(fill="x", pady=5)
        
        self.right_label = ttk.Label(self.gesture_frame, text=self.texts["right_arm"])
        self.right_label.grid(row=0, column=0, sticky="w", pady=2)
        self.right_combo = ttk.Combobox(self.gesture_frame, textvariable=self.right_arm_var, 
                                       values=[self.texts["next"], self.texts["previous"]], 
                                       state="readonly", width=15)
        self.right_combo.grid(row=0, column=1, padx=10, pady=2)
        self.right_combo.bind("<<ComboboxSelected>>", self.on_right_arm_changed)
        
        self.left_label = ttk.Label(self.gesture_frame, text=self.texts["left_arm"])
        self.left_label.grid(row=1, column=0, sticky="w", pady=2)
        self.left_combo = ttk.Combobox(self.gesture_frame, textvariable=self.left_arm_var, 
                                      values=[self.texts["next"], self.texts["previous"]], 
                                      state="readonly", width=15)
        self.left_combo.grid(row=1, column=1, padx=10, pady=2)
        self.left_combo.bind("<<ComboboxSelected>>", self.on_left_arm_changed)
        self.mirror_check = ttk.Checkbutton(self.gesture_frame, text=self.texts["mirror_camera"], 
                                            variable=self.mirror_var)
        self.mirror_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # Advanced settings
        self.advanced_frame = ttk.LabelFrame(main_frame, text=self.texts["advanced_config"], padding=10)
        self.advanced_frame.pack(fill="x", pady=5)
        
        self.sensitivity_label = ttk.Label(self.advanced_frame, text=self.texts["sensitivity"])
        self.sensitivity_label.grid(row=0, column=0, sticky="w", pady=2)
        self.sensitivity_scale = ttk.Scale(self.advanced_frame, from_=0.02, to=0.15, 
                                         variable=self.sensitivity_var, orient="horizontal", length=150)
        self.sensitivity_scale.grid(row=0, column=1, padx=10, pady=2)
        self.sensitivity_value = ttk.Label(self.advanced_frame, text="0.05")
        self.sensitivity_value.grid(row=0, column=2, pady=2)
        self.sensitivity_scale.configure(command=lambda v: self.sensitivity_value.configure(text=f"{float(v):.3f}"))
        
        self.cooldown_label = ttk.Label(self.advanced_frame, text=self.texts["cooldown"])
        self.cooldown_label.grid(row=1, column=0, sticky="w", pady=2)
        self.cooldown_scale = ttk.Scale(self.advanced_frame, from_=0.5, to=3.0, 
                                       variable=self.cooldown_var, orient="horizontal", length=150)
        self.cooldown_scale.grid(row=1, column=1, padx=10, pady=2)
        self.cooldown_value = ttk.Label(self.advanced_frame, text="1.0")
        self.cooldown_value.grid(row=1, column=2, pady=2)
        self.cooldown_scale.configure(command=lambda v: self.cooldown_value.configure(text=f"{float(v):.1f}"))
        
        # Additional options
        self.options_frame = ttk.LabelFrame(main_frame, text=self.texts["options"], padding=10)
        self.options_frame.pack(fill="x", pady=5)
        
        self.debug_check = ttk.Checkbutton(self.options_frame, text=self.texts["show_debug"], 
                                          variable=self.debug_var)
        self.debug_check.pack(anchor="w")
        self.keys_check = ttk.Checkbutton(self.options_frame, text=self.texts["use_arrows"], 
                                         variable=self.keys_var)
        self.keys_check.pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=15)
        
        self.test_button = ttk.Button(button_frame, text=self.texts["test_camera"], 
                                     command=self.test_camera)
        self.test_button.pack(side="left", padx=5)
        
        self.restore_button = ttk.Button(button_frame, text=self.texts["restore_defaults"], 
                                        command=self.restore_defaults)
        self.restore_button.pack(side="left", padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text=self.texts["cancel"], 
                                       command=self.root.destroy)
        self.cancel_button.pack(side="right", padx=5)
        
        self.start_button = ttk.Button(button_frame, text=self.texts["start"], 
                                      command=self.start_detection)
        self.start_button.pack(side="right", padx=5)
        
        self.save_button = ttk.Button(button_frame, text=self.texts["save_config"], 
                                     command=self.save_configuration)
        self.save_button.pack(side="right", padx=5)
        
        # Update window after creating all widgets
        self.root.update_idletasks()
        
        # Ensure initial values are correct
        self.update_slider_labels()
        
    def update_slider_labels(self):
        """Update slider labels with current values"""
        self.sensitivity_value.configure(text=f"{self.sensitivity_var.get():.3f}")
        self.cooldown_value.configure(text=f"{self.cooldown_var.get():.1f}")
        
    def on_right_arm_changed(self, event=None):
        """When right arm changes, automatically update left arm"""
        right_selection = self.right_arm_var.get()
        if right_selection == self.texts["next"]:
            self.left_arm_var.set(self.texts["previous"])
        else:
            self.left_arm_var.set(self.texts["next"])
            
    def on_left_arm_changed(self, event=None):
        """When left arm changes, automatically update right arm"""
        left_selection = self.left_arm_var.get()
        if left_selection == self.texts["next"]:
            self.right_arm_var.set(self.texts["previous"])
        else:
            self.right_arm_var.set(self.texts["next"])
        
    def center_window(self):
        """Center window on screen after calculating required size"""
        self.root.update_idletasks()
        
        # Get required size
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # Add extra padding to ensure everything is visible
        width = max(width + 50, 520)  # Minimum 520px width
        height = max(height + 30, 500)  # Minimum 500px height
        
        # Calculate center position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set geometry and center
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set minimum size to avoid becoming unusable
        self.root.minsize(520, 500)
        
    def change_language_by_name(self, language_options):
        """Change language based on selected full name"""
        selected_name = self.language_display_var.get()
        new_language_code = language_options.get(selected_name, "en")
        
        if new_language_code != self.current_language:
            # Save current values before change
            current_right_action = "next" if self.right_arm_var.get() == self.texts["next"] else "previous"
            current_left_action = "next" if self.left_arm_var.get() == self.texts["next"] else "previous"
            
            # Update language
            self.current_language = new_language_code
            self.language_var.set(new_language_code)  # Keep internal variable updated
            self.texts = TRANSLATIONS[new_language_code]
            
            # Update interface with new texts
            self.update_interface_texts()
            
            # Restore values with new translations
            self.right_arm_var.set(self.texts["next"] if current_right_action == "next" else self.texts["previous"])
            self.left_arm_var.set(self.texts["next"] if current_left_action == "next" else self.texts["previous"])

    def change_language(self, event=None):
        """Change interface language (original method kept for compatibility)"""
        new_language = self.language_var.get()
        if new_language != self.current_language:
            # Save current values before change
            current_right_action = "next" if self.right_arm_var.get() == self.texts["next"] else "previous"
            current_left_action = "next" if self.left_arm_var.get() == self.texts["next"] else "previous"
            
            # Update language
            self.current_language = new_language
            self.texts = TRANSLATIONS[new_language]
            
            # Update interface with new texts
            self.update_interface_texts()
            
            # Restore values with new translations
            self.right_arm_var.set(self.texts["next"] if current_right_action == "next" else self.texts["previous"])
            self.left_arm_var.set(self.texts["next"] if current_left_action == "next" else self.texts["previous"])
            
    def update_interface_texts(self):
        """Update all interface texts"""
        self.root.title(self.texts["title"])
        self.title_label.configure(text=self.texts["title"])

        # Update combobox values
        self.right_combo['values'] = [self.texts["next"], self.texts["previous"]]
        self.left_combo['values'] = [self.texts["next"], self.texts["previous"]]
        self.mirror_check.configure(text=self.texts["mirror_camera"])
        
        # Update widget texts
        self.gesture_frame.configure(text=self.texts["gesture_config"])
        self.right_label.configure(text=self.texts["right_arm"])
        self.left_label.configure(text=self.texts["left_arm"])
        
        self.advanced_frame.configure(text=self.texts["advanced_config"])
        self.sensitivity_label.configure(text=self.texts["sensitivity"])
        self.cooldown_label.configure(text=self.texts["cooldown"])
        
        self.options_frame.configure(text=self.texts["options"])
        self.debug_check.configure(text=self.texts["show_debug"])
        self.keys_check.configure(text=self.texts["use_arrows"])
        
        self.test_button.configure(text=self.texts["test_camera"])
        self.restore_button.configure(text=self.texts["restore_defaults"])
        self.save_button.configure(text=self.texts["save_config"])
        self.cancel_button.configure(text=self.texts["cancel"])
        self.start_button.configure(text=self.texts["start"])
        
        # Recalculate window size after language change
        self.root.after(10, self.center_window)
        
    def test_camera(self):
        """Test if camera is working"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror(self.texts["error"], self.texts["camera_error"])
        else:
            messagebox.showinfo(self.texts["success"], self.texts["camera_success"])
        cap.release()
        
    def restore_defaults(self):
        """Restore default settings"""
        next_text = self.texts["next"]
        previous_text = self.texts["previous"]
        
        self.right_arm_var.set(next_text)
        self.left_arm_var.set(previous_text)
        self.sensitivity_var.set(0.05)
        self.cooldown_var.set(1.0)
        self.debug_var.set(True)
        self.keys_var.set(True)
        self.mirror_var.set(True)
        
    def save_configuration(self):
        """Save settings without starting the program"""
        if not self._save_current_settings():
            return
            
        messagebox.showinfo(self.texts["success"], self.texts["config_saved_msg"])
        
    def _save_current_settings(self):
        """Helper method to save current settings"""
        # Convert translated texts back to internal values
        right_action = "next" if self.right_arm_var.get() == self.texts["next"] else "previous"
        left_action = "next" if self.left_arm_var.get() == self.texts["next"] else "previous"
        
        # Validation is no longer necessary since arms are always opposite automatically
        # but we keep it for safety in case of manual config file changes
        if right_action == left_action:
            messagebox.showwarning(self.texts["invalid_config"], self.texts["same_function"])
            return False
            
        # Save settings
        self.config.settings.update({
            "right_arm_action": right_action,
            "left_arm_action": left_action,
            "sensitivity": self.sensitivity_var.get(),
            "cooldown": self.cooldown_var.get(),
            "show_debug": self.debug_var.get(),
            "powerpoint_keys": self.keys_var.get(),
            "language": self.current_language,
            "mirror_camera": self.mirror_var.get()
        })
        self.config.save_config()
        return True
        
    def start_detection(self):
        """Save settings and start detection"""
        if not self._save_current_settings():
            return
            
        # Close window and start detection
        self.root.destroy()
        return True

class HandySlides:
    def __init__(self, config):
        self.config = config.settings
        self.last_press_time = 0
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
    def is_arm_raised(self, landmarks):
        """Detect if any arm is raised"""
        if not landmarks:
            return None
            
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

        if self.config["show_debug"]:
            print(f"L.Shoulder.y: {left_shoulder.y:.3f}, L.Wrist.y: {left_wrist.y:.3f}")
            print(f"R.Shoulder.y: {right_shoulder.y:.3f}, R.Wrist.y: {right_wrist.y:.3f}")

        sensitivity = self.config["sensitivity"]
        
        if left_wrist.y < left_shoulder.y - sensitivity:
            return "Left"

        if right_wrist.y < right_shoulder.y - sensitivity:
            return "Right"

        return None
    
    def execute_action(self, arm):
        """Execute action based on raised arm and configuration"""
        action = self.config.get(f"{arm.lower()}_arm_action")
        
        if self.config["powerpoint_keys"]:
            # Use keyboard arrows
            key = "right" if action == "next" else "left"
        else:
            # Use Page Up/Down
            key = "pagedown" if action == "next" else "pageup"
            
        pyautogui.press(key)
        
        if self.config["show_debug"]:
            print(f"{arm} arm raised! Action: {action} -> Key: {key}")
    
    def add_status_text(self, frame, text, color=(0, 255, 0)):
        """Add status text to frame"""
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, color, 2)
    
    def run(self):
        """Execute main detection loop"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera not working")
            return False

        print("HandySlides started! Press 'q' to exit.")
        print(f"Current configuration:")
        print(f"- Right arm: {self.config['right_arm_action']}")
        print(f"- Left arm: {self.config['left_arm_action']}")
        print(f"- Sensitivity: {self.config['sensitivity']}")
        print(f"- Cooldown: {self.config['cooldown']}s")

        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Error capturing frame.")
                    break

                # Mirror frame to be more intuitive
                if self.config["mirror_camera"]:
                    frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, 
                                                 self.mp_pose.POSE_CONNECTIONS)
                    
                    raised_arm = self.is_arm_raised(results.pose_landmarks)
                    current_time = time.time()
                    
                    if raised_arm and (current_time - self.last_press_time > self.config["cooldown"]):
                        self.execute_action(raised_arm)
                        self.last_press_time = current_time
                        self.add_status_text(frame, f"{raised_arm} arm detected!", (0, 255, 0))
                    elif raised_arm:
                        # Arm detected but still in cooldown
                        remaining = self.config["cooldown"] - (current_time - self.last_press_time)
                        self.add_status_text(frame, f"Cooldown: {remaining:.1f}s", (0, 165, 255))
                    else:
                        self.add_status_text(frame, "Ready - Raise your arm", (255, 255, 255))

                else:
                    self.add_status_text(frame, "Pose not detected", (0, 0, 255))
                
                cv2.imshow("HandySlides - Arm Gesture Control", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
        return True

def main():
    """Main function"""
    print("=== HandySlides - Slide Control by Gestures ===")
    
    # Show configuration window
    config_window = ConfigWindow()
    config_window.root.mainloop()
    
    # If window was closed without starting, exit
    try:
        config_window.root.state()
        return  # Window still exists, was cancelled
    except:
        pass  # Window was destroyed, continue
    
    # Start detection
    handyslides = HandySlides(config_window.config)
    handyslides.run()

if __name__ == "__main__":
    main()
