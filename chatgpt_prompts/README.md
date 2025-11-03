# ChatGPT Prompts for Thesis Writing

This folder contains all prompts and templates for writing your thesis with ChatGPT agent.

---

## 📝 FILES IN THIS FOLDER

### **1. CHATGPT_PROMPT_FOR_METHODOLOGY.md**
**Purpose:** Prompt for writing Data & Methodology sections  
**Status:** ✅ Used - Methodology section complete  
**Contains:**
- Instructions for Data section (4 subsections)
- Instructions for Methodology section (4 subsections)
- How to explain CNN for finance audience
- FOMC window definitions
- Style guidelines

---

### **2. CHATGPT_PROMPT_FOR_RESULTS.md** ⭐ **USE THIS NEXT**
**Purpose:** Prompt for writing Results section  
**Status:** ⏳ Ready to use  
**Contains:**
- Instructions for 4 results subsections
- Complete statistical reporting guidelines
- What to say about each table/figure
- How to interpret findings
- Addresses common questions

**How to use:**
1. Tell ChatGPT you finished Methodology
2. Attach your Introduction/Lit Review (that ChatGPT wrote earlier)
3. Paste the entire prompt from this file
4. ChatGPT writes Results section (~2,500-3,500 words)

---

### **3. RESULTS_SECTION_TEMPLATE_WITH_FIGURES.md**
**Purpose:** Shows exactly where to place each table and figure  
**Status:** ⏳ Use alongside prompt #2  
**Contains:**
- Template structure with [INSERT X] markers
- File paths for all tables and figures
- Pre-written captions
- Instructions for Word and LaTeX

**How to use:**
- Reference this while ChatGPT writes Results
- ChatGPT will include [INSERT TABLE X] markers
- You insert the actual files from `~/Desktop/Thesis_Results/thesis_output/`

---

## 🚀 QUICK START FOR RESULTS SECTION

**Step 1:** Tell ChatGPT you're ready for Results:
```
I finished Methodology. Now I need the Results section.
I'm attaching my Introduction/Lit Review (that you wrote).
Please read it and match that style.
```

**Step 2:** Give ChatGPT the prompt:
```
Copy entire contents of: CHATGPT_PROMPT_FOR_RESULTS.md
Paste into ChatGPT
```

**Step 3:** ChatGPT writes with markers:
```
Text text text...
[INSERT TABLE 5: FOMC Results]
More text text...
[INSERT FIGURE 4: FOMC Results]
```

**Step 4:** You insert the actual files from `thesis_output/`

---

## 📊 YOUR TABLES & FIGURES

**Location:** `~/Desktop/Thesis_Results/thesis_output/`

**Tables (LaTeX + CSV):**
- table1_sample_statistics
- table2_horizon_evaluation
- table3_portfolio_ew
- table4_portfolio_vw
- table5_fomc_results ⭐ MAIN
- table6_ew_vw_comparison

**Figures (PNG + PDF):**
- figure1_fomc_timeline
- figure2_decile_performance
- figure3_horizon_evaluation
- figure4_fomc_results ⭐ MAIN
- figure5_ew_vw_comparison
- figure6_cnn_architecture

---

## 🎯 NEXT PROMPTS (Coming Soon)

After Results is done, you'll need:
- **Discussion section** - Compare to literature, implications, limitations
- **Conclusion** - Summarize contributions and future work
- **Abstract** - Write last (summarize entire thesis)

**Want me to create these prompts?** Let me know!

---

## ✅ DOCUMENTATION STATUS

**Complete:** ✅ Methodology prompt  
**Ready:** ✅ Results prompt + template  
**Pending:** ⏳ Discussion, Conclusion, Abstract prompts

---

**All prompts are designed to:**
- Match your Introduction/Lit Review style
- Learn from papers in "Thesis Lit Review Sources"
- Use finance language (not CS jargon)
- Reference all tables and figures
- Report statistics properly
- Emphasize your three contributions

