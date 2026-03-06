import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk

from logic_engine import KnowledgeBase, Rule, forward_chaining


class SherlockGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sherlock Holmes: The Harrington Murder Mystery")
        self.geometry("1400x840")
        self.minsize(1200, 760)
        self.configure(bg="#0f0f10")

        self.case_stage = "Investigate"
        self.clues_found = set()
        self.story_log = []

        self.initialize_logic()
        self.setup_styles()
        self.create_widgets()
        self.update_display()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Dark.TFrame", background="#121214")
        style.configure("Panel.TFrame", background="#1a1b1f")
        style.configure("Card.TFrame", background="#202228")

        style.configure(
            "Title.TLabel",
            background="#121214",
            foreground="#d9b36c",
            font=("Georgia", 28, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#121214",
            foreground="#c6c6c6",
            font=("Georgia", 12),
        )
        style.configure(
            "Section.TLabel",
            background="#1a1b1f",
            foreground="#f2d8a5",
            font=("Georgia", 15, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background="#202228",
            foreground="#e8e8e8",
            font=("Consolas", 11),
            padding=10,
        )

        style.configure(
            "Action.TButton",
            background="#7c1f28",
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            focuscolor="none",
            font=("Segoe UI", 11, "bold"),
            padding=10,
        )
        style.map(
            "Action.TButton",
            background=[("active", "#a82d3a"), ("disabled", "#3f3f3f")],
            foreground=[("disabled", "#8f8f8f")],
        )

        style.configure(
            "Secondary.TButton",
            background="#2b2e34",
            foreground="#e4e4e4",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#3a3f48"), ("disabled", "#3f3f3f")],
            foreground=[("disabled", "#8f8f8f")],
        )

    def initialize_logic(self):
        initial_facts = {
            "Victim(Lord_Harrington)",
            "Location(Workshop)",
            "LockedFromInside(Workshop_Door)",
            "NoVisibleWounds(Lord_Harrington)",
            "Present(Cogsworth_Automaton)",
            "ClockStopped(10:17)",
            "PowerSurge(Workshop)",
        }
        self.kb = KnowledgeBase(initial_facts)

        self.rules = [
            Rule({"LockedFromInside(Workshop_Door)", "NoVisibleWounds(Lord_Harrington)"}, "Suggests(ImpossibleCrime)"),
            Rule({"Suggests(ImpossibleCrime)", "PowerSurge(Workshop)"}, "Suggests(ElectricalMethod)"),
            Rule({"Present(Cogsworth_Automaton)", "Location(Workshop)"}, "Witness(Cogsworth_Automaton)"),
            Rule({"Witness(Cogsworth_Automaton)", "Interrogated(Cogsworth)"}, "Testimony(Cogsworth_Reports_Device_Use)"),
            Rule({"Interrogated(Beatrice)", "Found(Financial_Motive)"}, "Suspicious(Beatrice)"),
            Rule({"Interrogated(Davies)", "Found(Bootprint_LabOil)"}, "Suspicious(Davies)"),
            Rule({"Found(Burned_Coil)", "Suggests(ElectricalMethod)"}, "Clue(Consciousness_Device)"),
            Rule({"Clue(Consciousness_Device)", "Found(Secret_Ledger)"}, "Activated(Consciousness_Device)"),
            Rule({"Activated(Consciousness_Device)", "Victim(Lord_Harrington)"}, "IsAlive(Lord_Harrington)"),
            Rule({"NoVisibleWounds(Lord_Harrington)"}, "IsDead(Lord_Harrington)"),
            Rule({"Suspicious(Davies)", "Clue(Consciousness_Device)"}, "HadAccess(Davies)"),
            Rule({"Suspicious(Beatrice)", "Found(Will_Alteration)"}, "HadMotive(Beatrice)"),
        ]

        self.deductions_log = forward_chaining(self.kb, self.rules)

    def create_widgets(self):
        top = ttk.Frame(self, style="Dark.TFrame", padding=(14, 10))
        top.pack(fill=tk.X)

        ttk.Label(top, text="Sherlock Holmes: The Harrington Murder Mystery", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            top,
            text="Uncover clues, interrogate suspects, and resolve the impossible crime.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        root_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        root_pane.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        left = ttk.Frame(root_pane, style="Panel.TFrame", padding=10)
        middle = ttk.Frame(root_pane, style="Panel.TFrame", padding=10)
        right = ttk.Frame(root_pane, style="Panel.TFrame", padding=10)
        root_pane.add(left, weight=4)
        root_pane.add(middle, weight=3)
        root_pane.add(right, weight=3)

        self._build_scene_panel(left)
        self._build_action_panel(middle)
        self._build_caseboard_panel(right)

    def _build_scene_panel(self, parent):
        ttk.Label(parent, text="Crime Scene", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        img_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        img_card.pack(fill=tk.BOTH, expand=False)

        try:
            image_path = "crime_scene.jpeg"
            img = Image.open(image_path)
            img = img.resize((620, 330), Image.Resampling.LANCZOS)
            self.crime_scene_photo = ImageTk.PhotoImage(img)
            tk.Label(img_card, image=self.crime_scene_photo, bd=0).pack(fill=tk.BOTH, expand=True)
        except Exception:
            placeholder = tk.Canvas(
                img_card,
                bg="#1f2024",
                height=330,
                highlightthickness=0,
            )
            placeholder.create_text(
                310,
                155,
                text="Workshop Crime Scene",
                fill="#d9b36c",
                font=("Georgia", 20, "bold"),
            )
            placeholder.create_text(
                310,
                195,
                text="(Add crime_scene.jpeg for artwork)",
                fill="#a0a0a0",
                font=("Consolas", 12),
            )
            placeholder.pack(fill=tk.BOTH, expand=True)

        status_card = ttk.Frame(parent, style="Card.TFrame")
        status_card.pack(fill=tk.X, pady=(10, 0))

        self.case_status_var = tk.StringVar()
        ttk.Label(status_card, textvariable=self.case_status_var, style="Status.TLabel", justify="left").pack(fill=tk.X)

        story_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        story_card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        ttk.Label(story_card, text="Narrative Log", style="Section.TLabel").pack(anchor="w")

        self.story_text = scrolledtext.ScrolledText(
            story_card,
            wrap=tk.WORD,
            bg="#121316",
            fg="#ececec",
            insertbackground="#ececec",
            font=("Consolas", 11),
            bd=0,
            relief=tk.FLAT,
            height=9,
        )
        self.story_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

    def _build_action_panel(self, parent):
        ttk.Label(parent, text="Investigative Actions", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        action_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        action_card.pack(fill=tk.X)

        self.action_buttons = {}
        actions = [
            ("Inspect Body", self.inspect_body),
            ("Search Workshop", self.search_workshop),
            ("Examine Desk", self.examine_desk),
            ("Interrogate Beatrice", self.question_beatrice),
            ("Interrogate Davies", self.question_davies),
            ("Interrogate Cogsworth", self.question_cogsworth),
            ("Reconstruct Timeline", self.reconstruct_timeline),
        ]

        for text, cmd in actions:
            btn = ttk.Button(action_card, text=text, command=cmd, style="Action.TButton")
            btn.pack(fill=tk.X, pady=4)
            self.action_buttons[text] = btn

        accuse_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        accuse_card.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(accuse_card, text="Final Accusation", style="Section.TLabel").pack(anchor="w")

        self.accused_var = tk.StringVar(value="Beatrice")
        suspect_box = ttk.Combobox(
            accuse_card,
            textvariable=self.accused_var,
            values=["Beatrice", "Davies", "Cogsworth"],
            state="readonly",
            font=("Consolas", 11),
        )
        suspect_box.pack(fill=tk.X, pady=(6, 8))

        self.btn_accuse = ttk.Button(
            accuse_card,
            text="Accuse Suspect",
            command=self.make_accusation,
            style="Secondary.TButton",
        )
        self.btn_accuse.pack(fill=tk.X)

        goals_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        goals_card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        ttk.Label(goals_card, text="Objectives", style="Section.TLabel").pack(anchor="w")

        self.objectives_text = scrolledtext.ScrolledText(
            goals_card,
            wrap=tk.WORD,
            bg="#121316",
            fg="#d9d9d9",
            font=("Consolas", 10),
            bd=0,
            relief=tk.FLAT,
            height=10,
        )
        self.objectives_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

    def _build_caseboard_panel(self, parent):
        ttk.Label(parent, text="Caseboard", style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        facts_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        facts_card.pack(fill=tk.BOTH, expand=True)
        ttk.Label(facts_card, text="Evidence & Facts", style="Section.TLabel").pack(anchor="w")

        self.facts_text = scrolledtext.ScrolledText(
            facts_card,
            wrap=tk.WORD,
            bg="#121316",
            fg="#cfe4ff",
            font=("Consolas", 10),
            bd=0,
            relief=tk.FLAT,
        )
        self.facts_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        ded_card = ttk.Frame(parent, style="Card.TFrame", padding=8)
        ded_card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        ttk.Label(ded_card, text="Holmes' Deductions", style="Section.TLabel").pack(anchor="w")

        self.deductions_text = scrolledtext.ScrolledText(
            ded_card,
            wrap=tk.WORD,
            bg="#121316",
            fg="#f3d59b",
            font=("Consolas", 10),
            bd=0,
            relief=tk.FLAT,
        )
        self.deductions_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

    def add_story(self, line):
        self.story_log.append(line)

    def add_fact(self, fact):
        if fact not in self.kb.get_facts():
            self.kb.add_fact(fact)
            return True
        return False

    def run_deduction_cycle(self):
        self.deductions_log = forward_chaining(self.kb, self.rules)
        self.update_display()

    def disable_action(self, action_text):
        btn = self.action_buttons.get(action_text)
        if btn:
            btn.config(state=tk.DISABLED)

    def inspect_body(self):
        self.add_story("Watson confirms no blade marks, no powder burns, and unusual neural scarring near the spine.")
        self.add_fact("Found(Neural_Scarring)")
        self.add_fact("Found(Cold_Body_No_BloodLoss)")
        self.disable_action("Inspect Body")
        self.run_deduction_cycle()

    def search_workshop(self):
        self.add_story("Behind a brass engine, Holmes discovers a burned coil and scorched wiring hidden under floor panels.")
        self.add_fact("Found(Burned_Coil)")
        self.add_fact("Found(Hidden_Wiring)")
        self.clues_found.add("workshop")
        self.disable_action("Search Workshop")
        self.run_deduction_cycle()

    def examine_desk(self):
        self.add_story("A concealed drawer reveals a secret ledger and a revised will drafted two nights ago.")
        self.add_fact("Found(Secret_Ledger)")
        self.add_fact("Found(Will_Alteration)")
        self.add_fact("Found(Financial_Motive)")
        self.disable_action("Examine Desk")
        self.run_deduction_cycle()

    def question_beatrice(self):
        self.add_story("Beatrice admits she argued with Harrington over inheritance but denies entering the workshop.")
        self.add_fact("Interrogated(Beatrice)")
        self.disable_action("Interrogate Beatrice")
        self.run_deduction_cycle()

    def question_davies(self):
        self.add_story("Davies confesses he trespassed earlier to calibrate a prototype and left oily bootprints.")
        self.add_fact("Interrogated(Davies)")
        self.add_fact("Found(Bootprint_LabOil)")
        self.disable_action("Interrogate Davies")
        self.run_deduction_cycle()

    def question_cogsworth(self):
        self.add_story("Cogsworth reports hearing 'transfer complete' before the power surge and collapse.")
        self.add_fact("Interrogated(Cogsworth)")
        self.disable_action("Interrogate Cogsworth")
        self.run_deduction_cycle()

    def reconstruct_timeline(self):
        self.add_story("Timeline reconstructed: power surge at 10:17, workshop sealed at 10:18, body found at 10:24.")
        self.add_fact("Timeline(Reconstructed)")
        self.add_fact("WindowOfCrime(7_Minutes)")
        self.disable_action("Reconstruct Timeline")
        self.run_deduction_cycle()

    def check_case_resolution(self):
        facts = self.kb.get_facts()
        return "IsAlive(Lord_Harrington)" in facts and "IsDead(Lord_Harrington)" in facts

    def make_accusation(self):
        suspect = self.accused_var.get()
        if not self.check_case_resolution():
            messagebox.showwarning(
                "Not Ready",
                "Holmes refuses to accuse anyone yet. Collect more evidence and complete key deductions first.",
            )
            return

        correct = suspect == "Davies"
        if correct:
            self.case_stage = "Solved"
            self.add_story("Holmes accuses Davies: the body died, but Harrington's consciousness was transferred.")
            self.add_story("Case Closed: Murder by engineered consciousness theft.")
            messagebox.showinfo(
                "Case Solved",
                "Brilliant deduction. Davies manipulated the transfer device and staged an impossible murder.",
            )
            for btn in self.action_buttons.values():
                btn.config(state=tk.DISABLED)
            self.btn_accuse.config(state=tk.DISABLED)
        else:
            self.case_stage = "Wrong Accusation"
            self.add_story(f"Holmes tests the accusation against {suspect}, but the logic collapses under scrutiny.")
            messagebox.showerror(
                "Incorrect Accusation",
                "The accusation is unsupported by the evidence. Re-evaluate the caseboard.",
            )

        self.update_display()

    def update_objectives(self):
        objectives = [
            ("Find physical evidence in the workshop", "Found(Burned_Coil)"),
            ("Interrogate all key witnesses", "Interrogated(Cogsworth)"),
            ("Uncover motive-related paperwork", "Found(Secret_Ledger)"),
            ("Trigger the consciousness contradiction", "IsAlive(Lord_Harrington)"),
            ("Make final accusation", None),
        ]

        self.objectives_text.config(state=tk.NORMAL)
        self.objectives_text.delete("1.0", tk.END)
        for title, fact in objectives:
            done = False
            if fact is None:
                done = self.case_stage == "Solved"
            else:
                done = fact in self.kb.get_facts()
            mark = "[x]" if done else "[ ]"
            self.objectives_text.insert(tk.END, f"{mark} {title}\n")
        self.objectives_text.config(state=tk.DISABLED)

    def update_display(self):
        facts = sorted(self.kb.get_facts())

        self.facts_text.config(state=tk.NORMAL)
        self.facts_text.delete("1.0", tk.END)
        self.facts_text.insert(tk.END, "\n".join(f"- {fact}" for fact in facts))
        self.facts_text.config(state=tk.DISABLED)

        self.deductions_text.config(state=tk.NORMAL)
        self.deductions_text.delete("1.0", tk.END)
        if self.deductions_log:
            self.deductions_text.insert(tk.END, "\n".join(self.deductions_log))
        else:
            self.deductions_text.insert(tk.END, "No new deductions yet.")

        if self.check_case_resolution():
            self.deductions_text.insert(
                tk.END,
                "\n\nCONTRADICTION DETECTED: Harrington is logically both dead and alive.",
            )
        self.deductions_text.config(state=tk.DISABLED)

        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete("1.0", tk.END)
        if self.story_log:
            self.story_text.insert(tk.END, "\n".join(self.story_log[-12:]))
        else:
            self.story_text.insert(tk.END, "Holmes arrives at Harrington Manor. The storm has not yet passed.")
        self.story_text.config(state=tk.DISABLED)

        clue_count = len([f for f in self.kb.get_facts() if f.startswith("Found(")])
        deduction_count = len(self.deductions_log)
        self.case_status_var.set(
            f"Case Stage: {self.case_stage}\\n"
            f"Evidence Collected: {clue_count} items\\n"
            f"New Deductions This Turn: {deduction_count}"
        )

        self.update_objectives()


if __name__ == "__main__":
    app = SherlockGame()
    app.mainloop()
