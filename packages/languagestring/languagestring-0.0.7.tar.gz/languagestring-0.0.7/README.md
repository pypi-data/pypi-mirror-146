# languagestring


<strong> To use: </strong>

<p> from languagestring import languagestring </p>
<p>ls = languagestring()</p>
<p> # get czech characters </p>
<p>ls.language_string('cz',case='lowercase')</p>
<p>'áčďéěíňóřšťúůýž'</p>


<strong>Working Languages: </strong>
<p> {
	"se" : "swedish",
	"fr" : "french",
	"de" : "german",
	"nl" : "dutch",
	"es" : "spanish",
	"pt" : "portuguese",
	"pl" : "polish",
	"cz" : "czech",
	"it" : "italian"
}</p>

<strong> Methods:</strong>
<p><strong>`language_string`</strong> - returns a string of the language characters.</p>
<p><strong>`language_array`</strong> - returns a list of the language characters.</p>
<p><strong>`alt_codes`</strong> - returns a list of the language alt codes.</p>
<p><strong>`description`</strong> - returns a list of the language description.</p>

<strong>Arguments:</strong>
<p>`case` is defaulted to all which returns lowercase, uppercase, and other characters.</p>
<p>`language` is the two letter iso that is the working language.</p>