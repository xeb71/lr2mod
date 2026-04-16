from __future__ import annotations
import builtins
import copy
from game.bugfix_additions.debug_info_ren import write_log
from game.main_character.perks.Perks_ren import perk_system
from game.main_character.mc_serums._mc_serum_definitions_ren import mc_serum_aura_obedience, mc_serum_aura_fertility
from game.main_character.MainCharacter_ren import mc
from game.game_roles.business_roles._duty_definitions_ren import work_for_tips_duty
from game.major_game_classes.serum_related.SerumDesign_ren import SerumDesign
from game.major_game_classes.serum_related.serums._serum_traits_T1_ren import antidote_trait
from game.major_game_classes.serum_related.serums.fetish_serums_ren import start_anal_fetish_quest, start_cum_fetish_quest, start_breeding_fetish_quest
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -3 python:
"""

class PersonStatMixin:
    """Mixin containing serum administration and all stat/skill change methods.

    Extracted from the Person god-class to reduce its size. All methods are
    instance methods that operate on ``self`` - they become part of Person
    via multiple inheritance and the Python MRO.

    **Assumed interface:** All methods below expect ``self`` to be a ``Person``
    instance and access the following attributes defined in ``Person.__init__``:
    ``love``, ``_sluttiness``, ``situational_sluttiness``, ``suggestibility``,
    ``suggest_bag``, ``happiness``, ``_obedience``, ``situational_obedience``,
    ``charisma``, ``charisma_debt``, ``int``, ``int_debt``, ``focus``,
    ``focus_debt``, ``hr_skill``, ``market_skill``, ``research_skill``,
    ``production_skill``, ``supply_skill``, ``sex_skills``, ``arousal``,
    ``max_arousal``, ``energy``, ``max_energy``, ``novelty``,
    ``serum_effects``, ``total_serum_count``, ``_serum_tolerance``,
    ``display_name``, ``title``, ``event_triggers_dict``.

    Ren'Py note: defined at ``init -3`` so that it is available when the
    ``Person`` class is assembled at ``init -2``.
    """

    def give_serum(self, serum: SerumDesign, add_to_log = True):
        if serum is None:
            return #We might have handed over no serum because we aren't producing any and a crisis was looking for one, or something similar.

        mc.stats.change_tracked_stat("Corruption", "Serums Given", 1)
        self.total_serum_count += 1

        # every 20 serums increase tolerance
        if self.total_serum_count % 20 == 0 and self.serum_tolerance < 4:
            self._serum_tolerance += 1
            mc.log_event(f"{self.display_name} serum tolerance increased", "float_text_yellow")

        serum = copy.copy(serum) #Take a copy so we aren't touching the reference we are handed.
        self.serum_effects.append(serum)
        self._applying_serum = True
        try:
            serum.run_on_apply(self, add_to_log)
        finally:
            self._applying_serum = False
        mc.listener_system.fire_event("give_random_serum", the_person = self)

    def apply_serum_study(self, add_to_log = True): #Called when the person is studied by the MC. Raises mastery level of all traits used in active serums by 0.2
        updated_traits = [trait.add_mastery(.2) for serum in self.serum_effects for trait in serum.traits]
        if any(updated_traits) and add_to_log:
            mc.log_event(f"Observed {self.display_name}", "float_text_blue")

    def change_suggest(self, amount: int, add_to_log = True): #This changes the base, usually permanent suggest. Use add_suggest_effect to add temporary, only-highest-is-used, suggestion values
        self.suggestibility += amount
        if add_to_log and amount != 0 and self.title:
            mc.log_event(f"{self.display_name}: Suggestibility increased permanently by {amount:+.0f}%", "float_text_blue")

    # monitor that mc serum suggest change amount does not exceed max_amt
    def change_modded_suggestibility(self, amount, max_amt = 30, add_to_log = True):
        if self.event_triggers_dict.get("mod_suggest_amt", 0) >= max_amt:
            return
        change_amount = amount
        if self.event_triggers_dict.get("mod_suggest_amt", 0) + amount > max_amt:
            change_amount = max_amt - self.event_triggers_dict.get("mod_suggest_amt", 0)
        self.change_suggest(change_amount, add_to_log = add_to_log)
        self.event_triggers_dict["mod_suggest_amt"] = self.event_triggers_dict.get("mod_suggest_amt", 0) + change_amount
        return

    def add_suggest_effect(self, amount: int, add_to_log = True):
        if amount > builtins.max(self.suggest_bag or [0]):
            self.change_suggest(-builtins.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the old max and...
            self.change_suggest(amount, add_to_log = False) #add our new suggest.
            if add_to_log and amount != 0 and self.title:
                mc.log_event(f"{self.display_name}: Suggestibility increased, by {amount:.0f}", "float_text_blue")
        # else:
        #     if add_to_log and amount != 0 and self.title:
        #         mc.log_event(f"{self.display_name}: Suggestibility {amount:.0f} lower than current {self.suggestibility} amount. Suggestibility unchanged.", "float_text_blue")
        self.suggest_bag.append(amount) #Add it to the bag, so we can check to see if it is max later.

    def remove_suggest_effect(self, amount: int):
        if amount in self.suggest_bag: # Avoid removing the "amount" if we don't actually have it in the bag.
            self.change_suggest(- builtins.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the max
            self.suggest_bag.remove(amount)
            self.change_suggest(builtins.max(self.suggest_bag or [0]), add_to_log = False) # Add the new max. If we were max, it is now lower, otherwise it cancels out.

    def max_stat_change_calc(self, max_change = 100, serum_check = None, stat_cap = 100):
        def get_max_suggestibility_modifier(suggestibility: int) -> int:
            if suggestibility == 0:
                return 0
            if suggestibility < 20:
                return builtins.int(suggestibility / 5.0)
            if suggestibility < 60:
                return 2 + builtins.int(suggestibility / 10.0)
            if suggestibility < 80:
                return 8 + builtins.int(suggestibility / 20.0)
            return 12

        max_change += get_max_suggestibility_modifier(self.suggestibility)
        if serum_check:
            max_change += (int(max_change * 1.2)) * int(self.active_serum_with_hidden_tag(serum_check))
        max_change = min(max_change, stat_cap)
        return max_change

    def change_love(self, amount: int, max_amount: int = 100, add_to_log = True, from_potion: bool = False, from_toy: bool = False) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Love", stat_cap = 100)
        amount = builtins.int(amount)

        if amount > 0:
            amount = builtins.int(round(amount * self.personality.love_gain_multiplier))
            if amount == 0:
                return 0
            if self.love > max_cap:
                return 0    # prevent decreasing of love
            # linger effect caused by serum trait (max 20% over calculated maximum)
            # min_change = 1 if self.love < min(100, int(max_amount * 1.2)) and self.active_serum_with_hidden_tag("Love") else 0
            if self.love + amount > max_cap:
                amount = max_cap - self.love

        if self.love + amount < -100:
            amount = -100 - self.love
        elif self.love + amount > 100:
            amount = 100 - self.love

        self.love += amount

        if add_to_log:
            if from_toy or getattr(self, '_applying_toy', False):
                _potion_suffix = " (toy)"
            elif from_potion or getattr(self, '_applying_serum', False):
                _potion_suffix = " (potion)"
            else:
                _potion_suffix = ""
            if amount == 0:
                mc.log_event(f"Love limit reached for interaction, Max:({max_cap:.0f}", "float_text_love")
            elif amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=red_heart_token_small}}{_potion_suffix}", "float_text_love")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=red_heart_token_small}}({max_cap:.0f}){_potion_suffix}", "float_text_love")
        return amount

    @property
    def sluttiness(self) -> int:
        return max(min(self._sluttiness + sum(amount for (amount, _) in self.situational_sluttiness.values()), 100), 0)

    def change_slut(self, amount: int, max_amount: int = 100, add_to_log = True, from_potion: bool = False, from_toy: bool = False) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Slut", stat_cap = 100)

        if amount > 0:
            amount = builtins.int(round(amount * self.personality.slut_gain_multiplier))
            if amount == 0:
                return 0
            if self._sluttiness > max_cap:  # prevent decreasing of sluttiness
                return 0
            # linger effect caused by serum trait (max 20% over calculated maximum)
            # min_change = 1 if self._sluttiness < min(100, int(max_amount * 1.2)) and self.active_serum_with_hidden_tag("Slut") else 0
            if self._sluttiness + amount > max_cap:
                amount = max_cap - self._sluttiness

        amount = builtins.int(amount)
        if self._sluttiness + amount < 0:
            amount = -self._sluttiness
        elif self._sluttiness + amount > 100:
            amount = 100 - self._sluttiness

        self._sluttiness += amount

        if add_to_log:
            if from_toy or getattr(self, '_applying_toy', False):
                _potion_suffix = " (toy)"
            elif from_potion or getattr(self, '_applying_serum', False):
                _potion_suffix = " (potion)"
            else:
                _potion_suffix = ""
            if amount == 0:
                mc.log_event(f"No Effect on Sluttiness, Max:({max_cap:.0f})", "float_text_slut")
            elif amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=gold_heart_token_small}}{_potion_suffix}", "float_text_slut")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=gold_heart_token_small}}({max_cap:.0f}){_potion_suffix}", "float_text_slut")
        return amount

    def add_situational_slut(self, source: str, amount: int, description = ""):
        self.situational_sluttiness[source] = (amount, description)

    def clear_situational_slut(self, source: str):
        self.situational_sluttiness.pop(source, None)

    def change_happiness(self, amount: int, max_amount: int = 300, add_to_log = True) -> int:
        max_amount = min(max_amount, 300)

        if amount > 0 and self.happiness > max_amount:  # prevent decreasing of happiness
            return 0

        if amount > 0:
            amount = builtins.int(round(amount * self.trance_multiplier * self.personality.happiness_gain_multiplier))
        else:
            amount = builtins.int(amount * self.trance_multiplier)
        if self.happiness + amount < 0:
            amount = 0 - self.happiness
        if self.happiness + amount > max_amount:
            amount = max_amount - self.happiness

        self.happiness += amount

        if add_to_log and amount != 0:
            mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=happy_token_small}}", "float_text_yellow")
        return amount

    @property
    def obedience(self) -> int:
        return max(min(self._obedience + sum(amount for (amount, _) in self.situational_obedience.values()), 300), 0)

    @obedience.setter
    def obedience(self, value: int):    # consider removal of direct setter
        write_log(f"{self.name} set obedience {value}")
        self._obedience = builtins.int(value)

    def change_obedience(self, amount: int, max_amount: int = 300, add_to_log = True, from_potion: bool = False, from_toy: bool = False) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Obedience", stat_cap = 300)
        amount = builtins.int(amount)

        if amount > 0:
            amount = builtins.int(round(amount * self.personality.obedience_gain_multiplier))
            if amount == 0:
                return 0
            if self._obedience > max_cap:
                return 0 # prevent decreasing of obedience
            # linger effect caused by serum trait (max 10% over calculated maximum -> say 140 obed with 10 from suggest would allow for max of 165 (150 + 10% of 150))
            #min_change = 1 if self._obedience < min(300, int(max_amount * 1.1)) and self.active_serum_with_hidden_tag("Obedience") else 0
            if self._obedience + amount > max_cap:
                amount = max_cap - self._obedience

        if self._obedience + amount < 0:
            amount = -self._obedience
        elif self._obedience + amount > max_cap:
            amount = max_cap - self._obedience

        self._obedience += amount

        if add_to_log and amount != 0: #If we don't know the title don't add it to the log, because we know nothing about the person
            if from_toy or getattr(self, '_applying_toy', False):
                _potion_suffix = " (toy)"
            elif from_potion or getattr(self, '_applying_serum', False):
                _potion_suffix = " (potion)"
            else:
                _potion_suffix = ""
            if amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=triskelion_token_small}}{_potion_suffix}", "float_text_obedience")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=triskelion_token_small}}({max_cap:.0f}){_potion_suffix}", "float_text_obedience")
        return amount

    def add_situational_obedience(self, source: str, amount: int, description = ""):
        self.situational_obedience[source] = (amount, description)

    def clear_situational_obedience(self, source: str):
        self.situational_obedience.pop(source, None)

    def _change_attr_with_debt(self, attr: str, debt_attr: str, amount: int, log_label: str, add_to_log: bool) -> int:
        '''
        Shared helper for attribute-change methods that track a debt when the
        value would fall below zero (charisma, intelligence, focus).
        '''
        value = getattr(self, attr) + getattr(self, debt_attr)
        setattr(self, debt_attr, 0)
        value += amount
        if value < 0:
            setattr(self, debt_attr, value)
            value = 0
        setattr(self, attr, value)
        if amount != 0 and add_to_log:
            mc.log_event(f"{self.display_name}: {amount:+.0f} {log_label}", "float_text_blue")
        return amount

    def change_cha(self, amount: int, add_to_log = True) -> int:
        return self._change_attr_with_debt("charisma", "charisma_debt", amount, "Charisma", add_to_log)

    def change_int(self, amount: int, add_to_log = True) -> int:
        return self._change_attr_with_debt("int", "int_debt", amount, "Intelligence", add_to_log)

    def change_focus(self, amount: int, add_to_log = True) -> int:
        return self._change_attr_with_debt("focus", "focus_debt", amount, "Focus", add_to_log)

    def _change_work_skill_attr(self, skill_attr: str, log_label: str, amount: int, add_to_log: bool) -> int:
        '''Shared helper for work-skill change methods (hr, market, research, production, supply).'''
        current = getattr(self, skill_attr)
        if amount + current < 0:
            amount = -current  # Min 0
        setattr(self, skill_attr, current + amount)
        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} {log_label}", "float_text_yellow")
        return amount

    def change_hr_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("hr_skill", "HR Skill", amount, add_to_log)

    def change_market_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("market_skill", "Market Skill", amount, add_to_log)

    @property
    def extra_market_skill(self) -> int:
        '''
        Returns the extra market skill of the person when enhanced by duty
        '''
        if not self.has_duty(work_for_tips_duty):
            return 0

        value = self.foreplay_sex_skill
        if self.sluttiness > 50:
            value += self.oral_sex_skill
        return value

    def change_research_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("research_skill", "Research Skill", amount, add_to_log)

    def change_production_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("production_skill", "Production Skill", amount, add_to_log)

    def change_supply_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("supply_skill", "Supply Skill", amount, add_to_log)

    def change_engineering_skill(self, amount: int, add_to_log = True):
        self._change_work_skill_attr("engineering_skill", "Engineering Skill", amount, add_to_log)

    @property
    def research_potential(self):
        result = (3 * self.int) + (self.focus) + (2 * self.research_skill) + 10
        if mc.business.head_researcher:
            bonus_percent = (mc.business.head_researcher.int - 2) * 0.05
            result *= (1.0 + bonus_percent) #Every point above int 2 gives a 5% bonus.
        else:
            result *= 0.9 #No head researcher is treated like int 0.
        return builtins.int(result)

    @property
    def human_resource_potential(self):
        return builtins.int(((3 * self.charisma) + self.int + (2 * self.hr_skill) + 15) / 5)

    @property
    def marketing_potential(self):
        if self.is_employee:
            return builtins.int((3 * self.charisma) + self.focus + (2 * (self.market_skill + self.extra_market_skill)) + 20)
        # for hiring screen assume duty that will apply bonus
        return builtins.int((3 * self.charisma) + self.focus + (2 * (self.market_skill + 5)) + 20)

    @property
    def production_potential(self):
        return builtins.int(((3 * self.focus) + self.int + (2 * self.production_skill) + 10))

    @property
    def supply_potential(self):
        return builtins.int(((5 * self.focus) + (3 * self.charisma) + (3 * self.supply_skill) + 20))

    @property
    def engineering_potential(self):
        return builtins.int(((3 * self.int) + self.focus + (2 * self.engineering_skill) + 10))

    def increase_work_skill(self, skill: int | str, max_value = 6, add_to_log = True):
        if skill == 0 or skill == "hr_skill":
            self.update_work_skill("hr_skill", min(max_value, self.hr_skill + 1), add_to_log = add_to_log)
        elif skill == 1 or skill == "market_skill":
            self.update_work_skill("market_skill", min(max_value, self.market_skill + 1), add_to_log = add_to_log)
        elif skill == 2 or skill == "research_skill":
            self.update_work_skill("research_skill", min(max_value, self.research_skill + 1), add_to_log = add_to_log)
        elif skill == 3 or skill == "production_skill":
            self.update_work_skill("production_skill", min(max_value, self.production_skill + 1), add_to_log = add_to_log)
        elif skill == 4 or skill == "supply_skill":
            self.update_work_skill("supply_skill", min(max_value, self.supply_skill + 1), add_to_log = add_to_log)

    def decrease_work_skill(self, skill: int | str, add_to_log = True):
        if skill in (0, "hr_skill"):
            self.update_work_skill("hr_skill", max(0, self.hr_skill - 1), add_to_log = add_to_log)
        elif skill in (1, "market_skill"):
            self.update_work_skill("market_skill", max(0, self.market_skill - 1), add_to_log = add_to_log)
        elif skill in (2, "research_skill"):
            self.update_work_skill("research_skill", max(0, self.research_skill - 1), add_to_log = add_to_log)
        elif skill in (3, "production_skill"):
            self.update_work_skill("production_skill", max(0, self.production_skill - 1), add_to_log = add_to_log)
        elif skill in (4, "supply_skill"):
            self.update_work_skill("supply_skill", max(0, self.supply_skill - 1), add_to_log = add_to_log)

    def update_work_skill(self, skill: int | str, score: int, add_to_log = True):
        skill_name = None
        if skill in (0, "hr_skill"):
            skill_name = "HR Skill"
            current = self.hr_skill
        elif skill in (1, "market_skill"):
            skill_name = "Market Skill"
            current = self.market_skill
        elif skill in (2, "research_skill"):
            skill_name = "Research Skill"
            current = self.research_skill
        elif skill in (3, "production_skill"):
            skill_name = "Production Skill"
            current = self.production_skill
        elif skill in (4, "supply_skill"):
            skill_name = "Supply Skill"
            current = self.supply_skill

        if skill_name is None:
            return

        if current == score:
            return
        if skill_name == "HR Skill":
            self.hr_skill = score
        elif skill_name == "Market Skill":
            self.market_skill = score
        elif skill_name == "Research Skill":
            self.research_skill = score
        elif skill_name == "Production Skill":
            self.production_skill = score
        elif skill_name == "Supply Skill":
            self.supply_skill = score

        if add_to_log:
            mc.log_event(f"{self.display_name} {skill_name.lower()} is now at level {score}", "float_text_green")

    def change_sex_skill(self, skill_name: str, amount: int, add_to_log = True):
        '''
        Change sex skill by passed amount -> skill cannot go lower than 0
        skill_name: "Foreplay", "Oral", "Vaginal", "Anal"
        '''
        if skill_name not in self.sex_skills:
            return

        self.update_sex_skill(skill_name, self.sex_skills[skill_name] + amount, add_to_log)

    def increase_sex_skill(self, skill: str, max_value = 5, add_to_log = True):
        '''
        Increase passed sex skill by 1 but not higher than max_value
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        max_value: maximum value for skill
        '''
        if skill not in self.sex_skills:
            return

        score = self.sex_skills[skill]
        if score < max_value:
            self.update_sex_skill(skill, score + 1, add_to_log)

    def decrease_sex_skill(self, skill: str, add_to_log = True):
        '''
        Decrease passed sex skill by 1 -> skill cannot go lower than 0
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        '''
        if skill not in self.sex_skills:
            return

        score = self.sex_skills[skill]
        if score > 0:
            self.update_sex_skill(skill, score - 1, add_to_log)

    def update_sex_skill(self, skill: str, score, add_to_log = True):
        '''
        Update sex skill to passed value
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        score: new value for skill (cannot go lower than 0)
        '''
        if skill not in self.sex_skills:
            return

        current = self.sex_skills[skill]
        if current == score:
            return

        self.sex_skills[skill] = max(score, 0)
        if add_to_log:
            mc.log_event(f"{self.display_name} {skill.lower()} skill is now at level {score}", "float_text_green")

    def change_stats(self, obedience: int | None = None, happiness: int | None = None, arousal: int | None = None, love: int | None = None,
                    slut: int | None = None, max_slut: int = 100, max_love: int = 100, max_obedience: int = 300,
                    energy: int | None = None, novelty: int | None = None, add_to_log = True):
        message = []
        if happiness is not None:
            amount = self.change_happiness(happiness, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} {{image=happy_token_small}}")
        if obedience is not None and obedience != 0:
            amount = self.change_obedience(obedience, max_obedience, add_to_log = False)

            max_cap = self.max_stat_change_calc(max_change = max_obedience, serum_check = "Obedience")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=triskelion_token_small}}")   #Don't show cap if we are subtracting
            else:
                message.append(f"{amount:+.0f} {{image=triskelion_token_small}} ({max_cap:.0f})")
        if arousal is not None:
            amount = self.change_arousal(arousal, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} {{image=arousal_token_small}}")
        if love is not None and love != 0:
            amount = self.change_love(love, max_love, add_to_log = False)
            max_cap = self.max_stat_change_calc(max_change = max_love, serum_check = "Love")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=red_heart_token_small}}")
            else:
                message.append(f"{amount:+.0f} {{image=red_heart_token_small}}({max_cap:.0f})")
        if slut is not None and slut != 0:
            amount = self.change_slut(slut, max_slut, add_to_log = False)
            #if amount != 0:
            max_cap = self.max_stat_change_calc(max_change = max_slut, serum_check = "Slut")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=gold_heart_token_small}}")
            else:
                message.append(f"{amount:+.0f} {{image=gold_heart_token_small}}({max_cap:.0f})")
        if energy is not None:
            amount = self.change_energy(energy, add_to_log = False)
            if amount != 0:
                percentage = amount * 1.0 / max(self.max_energy, 1)
                message.append(f"{percentage:+.0%} {{image=energy_token_small}}")
        if novelty is not None:
            amount = self.change_novelty(novelty, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} Novelty")
        if add_to_log and message:
            mc.log_notification(f"{self.display_name}: {' '.join(message)}", "float_text_yellow")

    def change_arousal(self, amount: int, add_to_log = True, toy_amount: int = 0) -> int:
        amount = builtins.int(builtins.round(amount))
        toy_amount = builtins.int(builtins.round(toy_amount))
        if self.arousal + amount < 0:
            amount = 0 - self.arousal

        self.arousal += amount
        if add_to_log and amount != 0:
            _toy_suffix = f" ({toy_amount:+.0f} toy)" if toy_amount != 0 else ""
            mc.log_notification(f"{self.display_name}: {amount:+.0f}{_toy_suffix} {{image=arousal_token_small}}", "float_text_red")
        return amount

    def reset_arousal(self):
        base_arousal = self.sluttiness / 10.0
        base_arousal += self.opinion.masturbating
        base_arousal += self.opinion.showing_her_tits
        base_arousal += self.opinion.showing_her_ass
        base_arousal += self.opinion.not_wearing_underwear

        if base_arousal < 0:
            base_arousal = 0

        self.arousal = builtins.int(base_arousal)

    def change_max_arousal(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.max_arousal < 20:
            amount = -(self.max_arousal - 20)

        self.max_arousal += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Max Arousal", "float_text_red")
        return amount

    def change_novelty(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.novelty > 100:
            amount = 100 - self.novelty
        elif amount + self.novelty < 0:
            amount = self.novelty
        self.novelty += amount

        if add_to_log and amount != 0:
            mc.log_notification(f"{self.display_name}: {amount:+.0f} Novelty", "float_text_yellow")
        return amount

    def change_energy(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.energy > self.max_energy:
            amount = self.max_energy - self.energy
        elif amount + self.energy < 0:
            amount = -self.energy

        self.energy += amount

        if add_to_log and amount != 0:
            percentage = amount * 1.0 / max(self.max_energy, 1)
            mc.log_notification(f"{self.display_name}: {percentage:+.0%} {{image=energy_token_small}}", "float_text_energy")
        return amount

    def change_max_energy(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.max_energy < 20:
            amount = -(self.max_energy - 20)
        if amount + self.max_energy > 200:  # max energy for person 200
            amount = 200 - self.max_energy

        self.max_energy += amount

        if self.energy > self.max_energy: #No having more energy than max
            self.energy = self.max_energy

        if add_to_log and amount != 0:
            percentage = amount * 1.0 / max(self.max_energy, 1)
            mc.log_event(f"{self.display_name}: {percentage:+.0%} Max Energy", "float_text_energy")
        return amount

