// never stops running
let condition = true

while (condition) {
    console.log("Looping...");

    if (document.querySelector('.load-more') !== null) {
        window.scrollTo(0, document.body.scrollHeight);
        document.querySelector('.load-more').click();
        console.log('Load More button clicked.');
    } else {
        condition = False;
    }
}


# never stops running
while (true) {
    console.log("Looping...");

    if (document.querySelector('.load-more') !== null) {
        window.scrollTo(0, document.body.scrollHeight);
        document.querySelector('.load-more').click();
        console.log('Load More button clicked.');
    } else {
        break;
    }
}







    try {
        window.scrollTo(0, document.body.scrollHeight);
        document.querySelector('.load-more').click();
        console.log('Load More button clicked.');

    } catch (error) {
        console.error("An error occurred:", error);
        
    } finally {
        break;
    }
})
    try {
        window.scrollTo(0, document.body.scrollHeight);
        document.querySelector('.load-more').click();
        console.log('Load More button clicked.');

    } catch (error) {
        console.error("An error occurred:", error);
        
    } finally {
        break;
    }
}

while (document.querySelector('.load-more') !== null) {

    try {
        window.scrollTo(0, document.body.scrollHeight);
        document.querySelector('.load-more').click();
        console.log('Load More button clicked.');

    } catch (error) {
        console.error("An error occurred:", error);
        
    } finally {
        break;
    }
}