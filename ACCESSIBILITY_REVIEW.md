# Accessibility Review — Team 11 Inventory Management System

## 1. Overview

**Project:** Inventory Management System — Team 11  
**Technology:** Python 3.11, Command-Line Interface (CLI), JSON  
**Review Scope:** Accessibility of terminal interaction, output readability, input validation, error messages, and assistive technology compatibility.

### Objective

The purpose of this review is to identify potential accessibility barriers and recommend improvements that help users with different abilities and levels of technical experience operate the inventory management system.

This review focuses on the actual CLI implementation. Web-specific accessibility criteria are included only as future considerations if the project is developed into a web-based dashboard.

## 2. Accessibility Review Findings

| ID | Area | Potential Issue | Recommended Improvement | Priority |
|---|---|---|---|---|
| A11Y-01 | Input Instructions | Users may not understand the required input format. | Display clear prompts, field names, units, and examples. | High |
| A11Y-02 | Error Messages | Technical or unclear errors may prevent users from recovering. | Explain what went wrong and how to correct the input. | High |
| A11Y-03 | Color Independence | Low-stock alerts may rely on red or green indicators. | Include explicit text labels such as `[LOW STOCK]` and `[NORMAL]`. | High |
| A11Y-04 | Output Readability | Inventory results may be difficult to scan. | Use consistent headings, spacing, column labels, and number formatting. | Medium |
| A11Y-05 | Data Validation | Invalid input may confuse users or cause unintended changes. | Validate input before updating stock or saving data. | High |
| A11Y-06 | Keyboard Operation | Users may need clearer instructions for navigation and exiting. | Document available commands and provide predictable keyboard interaction. | Medium |
| A11Y-07 | Thai Language Support | Thai characters may display incorrectly in some terminal environments. | Use UTF-8-compatible output and test Thai text in the target terminal. | Medium |
| A11Y-08 | Assistive Technology | Output may not be easy to navigate with a screen reader. | Prefer meaningful text, logical output order, and clear status messages. | Medium |
| A11Y-09 | Stock Reports | Users may confuse stock quantities, thresholds, and monetary values. | Label each value and display appropriate units and currency. | Medium |

**Important:** These are potential accessibility risks and recommended improvements, not confirmed defects. Actual findings must be recorded after testing the application.

## 3. Recommended Improvements

### 3.1 Clear Input Instructions

Every input prompt should explain what the user needs to enter.

Example:

```text
Enter product ID:
Enter quantity to add (units):
Enter stock threshold (units):
```

Prompts should use consistent terminology and provide examples when the expected format is not obvious.

### 3.2 Helpful Error Messages

Error messages should explain the problem in plain language and help users recover.

Example:

```text
Error: Insufficient stock.
Available quantity: 5 units.
Requested quantity: 8 units.
Please enter a quantity of 5 units or less.
```

Invalid input must not change stock quantities or persist invalid data.

### 3.3 Low-Stock Alerts Without Color Dependence

Low-stock status must remain understandable when terminal colors are unavailable or difficult to distinguish.

Example:

```text
Product: Keyboard
Current Stock: 2 units
Threshold: 5 units
Status: LOW STOCK — Reorder recommended.
```

The system should apply the documented rule:

`stock_quantity <= threshold`

### 3.4 Readable Inventory Reports

Reports should use consistent labels and formatting.

Example:

```text
Inventory Summary
-----------------
Product: Keyboard
Category: Accessories
Current Stock: 2 units
Stock Threshold: 5 units
Status: LOW STOCK
```

Monetary reports should clearly distinguish unit price, stock quantity, category value, and total inventory value where those fields are supported by the implementation.

### 3.5 Keyboard and Assistive Technology Support

- Document available commands and navigation instructions.
- Ensure prompts and responses follow a logical sequence.
- Avoid relying exclusively on color, symbols, or visual alignment.
- Test terminal output with a compatible screen reader where available.
- Ensure users can understand how to recover from invalid input or exit the application.

## 4. Accessibility Test Plan

| Test ID | Test Scenario | Expected Result | Status |
|---|---|---|---|
| A11Y-T01 | Enter a negative stock quantity. | Input is rejected with a clear explanation; stock remains unchanged. | Not tested |
| A11Y-T02 | Issue more stock than is available. | Transaction is rejected and available stock is reported. | Not tested |
| A11Y-T03 | Check an item whose quantity equals its threshold. | Item is identified as low stock. | Not tested |
| A11Y-T04 | Read alerts without terminal colors. | Status remains understandable from text alone. | Not tested |
| A11Y-T05 | Display Thai product names and messages. | Thai characters are readable in the target terminal. | Not tested |
| A11Y-T06 | Review inventory output using keyboard navigation. | Output and available commands are understandable without a mouse. | Not tested |
| A11Y-T07 | Test with a supported screen reader. | Important prompts, values, and status messages can be understood. | Not tested |
| A11Y-T08 | Review category and inventory value reports. | Labels, units, and totals are distinguishable. | Not tested |

## 5. Acceptance Criteria

The accessibility improvements can be considered complete when:

- [ ] Input prompts clearly identify required values and units.
- [ ] Error messages explain the issue and how to recover.
- [ ] Low-stock and normal states are distinguishable without color.
- [ ] Invalid operations do not change stock or save invalid data.
- [ ] Thai text is readable in the supported terminal environment.
- [ ] Reports identify quantities, thresholds, and monetary values clearly.
- [ ] Keyboard interaction and exit instructions are documented.
- [ ] Screen-reader compatibility has been tested where applicable.
- [ ] Test results and evidence are recorded for each completed check.

## 6. Testing Evidence

For every completed test, record:

- Test date and tester.
- Operating system and terminal environment.
- Test input and execution steps.
- Expected result and actual result.
- Pass/fail status.
- Screenshot, terminal output, or other supporting evidence.
- Corrective action and retest result, if applicable.

Do not mark a test as passed until its result has been verified.

## 7. Standards and References

This review uses general accessibility principles as guidance, including understandable content, keyboard operability, and avoiding color as the only means of conveying information.

- [W3C Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C Accessibility Principles](https://www.w3.org/WAI/fundamentals/accessibility-principles/)

WCAG is a web content standard. Its web-specific success criteria should not be used to claim that a CLI application is WCAG-conformant. The principles are used here as guidance, with tests adapted to the actual terminal interface.

## 8. Conclusion

This review identifies practical improvements for making Team 11's inventory management CLI easier to understand and operate. The main priorities are clear input instructions, helpful error recovery, text-based stock alerts, readable reports, and reliable handling of invalid data.

The next step is to run the documented tests against the actual implementation, record the evidence, and update the review based on verified results. Accessibility status should be reported as confirmed only after the relevant checks have been completed.
