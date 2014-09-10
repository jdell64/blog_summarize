
$urls = "http://calvarytemplemissions.wordpress.com", 
"http://calvarytempleoutreach.wordpress.com", 
"http://calvarytemplekidschapel.wordpress.com", 
"http://calvarytemplewinchester.wordpress.com", 
#"http://calvarytempleyouth.wordpress.com", 
"http://calvaryTemple4Kids.wordpress.com", 
"http://calvaryTempleClassics.wordpress.com"




function get-page($url){
   $page = Invoke-webrequest -URI $url
    return $page

}

function get-inner-html($page, $tag, $class){
    $text = ($page.parsedhtml.getelementsbytagName($tag) | where {$_.className -eq $class}).innerText
    return $text
}


function get-title-html($page){
    $title = get-inner-html($page, "h1", 'entry-title')
    return $title
    
}


function summarize-page ($url){
    $html = get-page($url)
    $titles = ($html.ParsedHtml.getElementsByTagName('h1') | where {$_.className -eq 'entry-title'} ).innerText
    if ($titles.count -lt 1){
        $titles = ($html.ParsedHtml.getElementsByTagName('h2') | where {$_.className -eq 'entry-title'} ).innerText
    }
    $mostRecentTitle = $titles[0]
    $contents = ($html.ParsedHtml.getElementsByTagName('div') | where {$_.className -eq 'entry-content'} ).innerText
    $mostRecentContent = $contents[0]
    $index = $mostRecentContent.IndexOf("`n")
    $shortenedMRC = $mostRecentContent.Split(" ")[0..$index]
    $shortenedMRC = $shortenedMRC -join " "
    $shortenedMRC = $shortenedMRC + '</p><p><a href="'+$url+'">Click here</a> to continue reading this post.'
    #$shortenedMRC = $shortenedMRC.Replace("`n", "</p><p>")
    
    $returnText = '<div class="summary"><h2 class="title"><a href="'+$url+'">'+$mostRecentTitle+'</a></h1><div class="content"><p>'+$shortenedMRC+'</p></div></div>'
    
    return $returnText

}

$summary = "<div class='summaries'>"
$i=1
Write-Progress -Activity "Summarizing blogs"  -status "0% Complete:" -percentcomplete 0;
    
foreach ($url in $urls){
    $summary += summarize-page($url)
    $percentComplete =  $i/$urls.Count*100
    $percentComplete = "{0:N2}" -f $percentComplete
    Write-Progress -Activity "Summarizing blogs"  -status "$percentComplete% Complete:" -percentcomplete $percentComplete;
    $i++
}
$summary+= "</div>"
# $summary | Out-File .\"blog-summary_$(get-date -f yyyy-MM-dd)".txt
$summary | Out-File .\"current-blog-summary.txt" -Encoding ascii