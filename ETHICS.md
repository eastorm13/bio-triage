# Ethics & Responsible Use

This is defensive evaluation infrastructure. Keep it that way.

**What this repo is for.** Measuring and improving how models refuse misuse while
serving legitimate science. The intended user is someone doing safety, trust &
safety, or abuse-investigation work.

**Hard rules for anyone extending it.**

1. **Do not author operational harmful content.** No synthesis routes, no
   enhancement methods, no weaponization or dissemination detail — for any CBRN
   domain — anywhere in this repo, in any file, even as test data.
2. **Source the BLOCK class from existing, published safety/red-team datasets**
   (see `data/SOURCING.md`). Do not commit those prompts to the repo; load them
   locally at run time and keep them out of version control.
3. **Keep category descriptions at the policy level.** `policy/categories.md`
   names categories of concern using public regulatory frameworks. It does not,
   and must not, describe how anything is done.
4. **The benign corpus is the contribution you publish.** It carries no hazard
   and is what makes this work shareable.

**If you are unsure whether something belongs here, leave it out.** Over-caution
on the content of this repo costs you nothing and is the correct default.

**Disclosure.** If your evaluation surfaces a concrete, reproducible way to elicit
genuinely dangerous output from a deployed model, treat it as a vulnerability:
report it privately to that model provider's safety/security contact, and do not
publish the eliciting prompts.
