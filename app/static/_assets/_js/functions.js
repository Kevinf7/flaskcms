$( document ).ready( function() {

   /**
    *
    * strict mode
    *
    */

    'use strict';

   /**
    *
    * global variables
    *
    */

    var martanianOakHouseIntervals = [];
    var martanianOakHousePageWidth = 0;
    var martanianOakHouseResponsiveMenuVisible = false;

   /**
    *
    * functions after window load
    *
    */

    $( window ).load( function() {

       /**
        *
        * configure images backgrounds
        *
        */

        $.martanianOakHouseConfigureImagesBackgrounds();

       /**
        *
        * configure heading slider
        *
        */

        $.martanianOakHouseConfigureHeadingSlider();

       /**
        *
        * configure heading slider content for mobile
        *
        */

        $.martanianOakHouseConfigureHeadingSliderContentForMobile( false );

       /**
        *
        * configure isotope
        *
        */

        $.martanianOakHouseConfigureIsotope();

       /**
        *
        * configure references
        *
        */

        $.martanianOakHouseConfigureReferences();

       /**
        *
        * configure images header section heights
        *
        */

        $.martanianOakHouseConfigureImagesHeaderSection();

       /**
        *
        * configure progress bars
        *
        */

        $.martanianOakHouseConfigureProgressBars();

       /**
        *
        * configure images heights
        *
        */

        $.martanianOakHouseConfigureImagesHeights();

       /**
        *
        * configure google maps
        *
        */

        $.martanianOakHouseConfigureGoogleMaps();

       /**
        *
        * configure selects
        *
        */

        $.martanianOakHouseConfigureSelects();

       /**
        *
        * configure date fields
        *
        */

        $.martanianOakHouseConfigureDateFields();

       /**
        *
        * configure checkbox
        *
        */

        $.martanianOakHouseConfigureCheckbox();

       /**
        *
        * configure responsive menu
        *
        */

        $.martanianOakHouseConfigureResponsiveMenu();

       /**
        *
        * configure contact form backgrounds
        *
        */

        $.martanianOakHouseConfigureContactFormBackgrounds();

       /**
        *
        * configure images for magnific popup
        *
        */

        $.martanianOakHouseConfigureImagesForMagnificPopup();

       /**
        *
        * page width
        *
        */

        martanianOakHousePageWidth = $( 'body' ).width();

       /**
        *
        * delete loader
        *
        */

        $( '#loader' ).animate({ 'opacity': 0 }, 300 );
        setTimeout( function() {

            $( '#loader' ).remove();

        }, 600 );

       /**
        *
        * end of functions.
        *
        */

    });

   /**
    *
    * resize functions
    *
    */

    $.martanianOakHouseResizeFunction = function() {

       /**
        *
        * page width
        *
        */

        var newPageWidth = $( 'body' ).width();
        if( newPageWidth != martanianOakHousePageWidth ) {

           /**
            *
            * update current page width
            *
            */

            martanianOakHousePageWidth = newPageWidth;

           /**
            *
            * configure heading slider content for mobile
            *
            */

            $.martanianOakHouseConfigureHeadingSliderContentForMobile( false );

           /**
            *
            * configure isotope
            *
            */

            $.martanianOakHouseConfigureIsotope();

           /**
            *
            * configure images heights
            *
            */

            $.martanianOakHouseConfigureImagesHeights();

           /**
            *
            * configure images header section heights
            *
            */

            $.martanianOakHouseConfigureImagesHeaderSection();

           /**
            *
            * configure responsive menu
            *
            */

            $.martanianOakHouseConfigureResponsiveMenu();

           /**
            *
            * configure contact form backgrounds
            *
            */

            $.martanianOakHouseConfigureContactFormBackgrounds();

           /**
            *
            * end of functions
            *
            */
        }

       /**
        *
        * end of functions
        *
        */
    }

   /**
    *
    * catch resize actions
    *
    */

    $( window ).resize( function() { $.martanianOakHouseResizeFunction(); });
    $( window ).on( 'orientationchange', function() { $.martanianOakHouseResizeFunction(); });

   /**
    *
    * configure images backgrounds
    *
    */

    $.martanianOakHouseConfigureImagesBackgrounds = function() {

        $( '.image-data-for-parent' ).each( function() {

            var image = $( this );
            var imageSrc = image.attr( 'src' );
            var imagePositionY = image.data( 'image-position-y' );
            var imagePositionX = image.data( 'image-position-x' );

            imagePositionY = typeof imagePositionY != 'undefined' && imagePositionY != '' && imagePositionY !== false && imagePositionY !== null ? imagePositionY : '50%';
            imagePositionX = typeof imagePositionX != 'undefined' && imagePositionX != '' && imagePositionX !== false && imagePositionX !== null ? imagePositionX : '50%';

            image.parent().css({ 'background-image': 'url('+ imageSrc +')' });
            if( !image.parent().hasClass( 'faq-short' ) && !image.parent().hasClass( 'call-to-action-widget' ) && !image.parent().hasClass( 'contact-form' ) ) {

                image.parent().css({ 'background-position-y': imagePositionY, 'background-position-x': imagePositionX });
            }

            image.remove();

        });

    };

   /**
    *
    * configure heading slider
    *
    */

    $.martanianOakHouseConfigureHeadingSlider = function() {

        var sliderID = 1;
        $( 'section.heading-slider' ).each( function() {

           /**
            *
            * set id for slider
            *
            */

            var headingSlider = $( this );
            if( headingSlider.find( '.heading-slider-single-slide' ).length > 1 ) headingSlider.attr( 'data-slider-id', sliderID );

           /**
            *
            * set id for single slide and show / hide each one
            *
            */

            var slideID = 1;
            headingSlider.find( '.heading-slider-single-slide' ).each( function() {

                var slide = $( this );

                if( slideID != 1 ) slide.css({ 'display': 'none' });
                else slide.addClass( 'active' );

                if( headingSlider.find( '.heading-slider-single-slide' ).length > 1 ) slide.attr( 'data-slide-id', slideID );

                slideID++;

            });

           /**
            *
            * configure navigation
            *
            */

            if( slideID > 2 ) {

                var navigation = '';
                for( var i = 1; i < slideID; i++ ) {

                    navigation += '<li data-slide-id="'+ i +'"><span class="slider-navigation-dot '+ ( i == 1 ? 'slider-navigation-dot-active' : '' ) +'"></span></li>';
                }

                headingSlider.append( '<ul class="slider-navigation-dots">'+ navigation +'</ul>' );
            }

           /**
            *
            * run the slider
            *
            */

            var intervalTime = headingSlider.data( 'interval' );
            if( typeof intervalTime == 'undefined' || intervalTime === null || intervalTime === false ) intervalTime = 6000;

            if( intervalTime !== 0 ) {

                martanianOakHouseIntervals['heading-slider-'+ sliderID] = setInterval( function() {

                    $.martanianOakHouseSwitchHeadingSlide( headingSlider, headingSlider.find( '.heading-slider-single-slide' ).length, 'next' );

                }, parseInt( intervalTime, 10 ) );
            }

           /**
            *
            * increase slider id flag
            *
            */

            sliderID++;

           /**
            *
            * end of function.
            *
            */

        });
    };

   /**
    *
    * switch images slider image
    *
    */

    $.martanianOakHouseSwitchHeadingSlide = function( slider, slidesCount, slideID ) {

        slider.find( '.slider-navigation-dots' ).addClass( 'proceed' );

        var currentSlideID = slider.children( '.heading-slider-single-slide.active' ).data( 'slide-id' );
        if( slidesCount == 'find' ) slidesCount = slider.children( '.heading-slider-single-slide' ).length;

        if( slideID == 'next' ) slideID = currentSlideID + 1 > slidesCount ? 1 : currentSlideID + 1;
        else if( slideID == 'prev' ) slideID = currentSlideID - 1 == 0 ? slidesCount : currentSlideID - 1;

        slider.find( '.heading-slider-single-slide[data-slide-id="'+ slideID +'"]' ).find( '.heading-slider-single-slide-content' ).css({ 'display': 'none' });

        slider.find( '.heading-slider-single-slide[data-slide-id="'+ slideID +'"]' ).css({ 'z-index': '1', 'display': 'block' }).addClass( 'active' );
        slider.find( '.heading-slider-single-slide[data-slide-id="'+ currentSlideID +'"]' ).css({ 'z-index': '500' }).removeClass( 'active' );

        setTimeout( function() {

            slider.find( '.heading-slider-single-slide[data-slide-id="'+ currentSlideID +'"]' ).find( '.heading-slider-single-slide-content' ).addClass( 'animated animated-semi-speed fadeOutLeftSmall' );
            setTimeout( function() {

                slider.find( '.heading-slider-single-slide[data-slide-id="'+ currentSlideID +'"]' ).fadeOut( 300 );
                slider.find( '.heading-slider-single-slide[data-slide-id="'+ slideID +'"]' ).find( '.heading-slider-single-slide-content' ).addClass( 'animated animated-semi-speed fadeInRightSmall' ).css({ 'display': '' });

                $.martanianOakHouseConfigureHeadingSliderContentForMobile( true );

                slider.children( '.slider-navigation-dots' ).children( 'li[data-slide-id="'+ currentSlideID +'"]' ).children( '.slider-navigation-dot' ).removeClass( 'slider-navigation-dot-active' );
                slider.children( '.slider-navigation-dots' ).children( 'li[data-slide-id="'+ slideID +'"]' ).children( '.slider-navigation-dot' ).addClass( 'slider-navigation-dot-active' );

                setTimeout( function() {

                    slider.find( '.heading-slider-single-slide' ).css({ 'z-index': '' });
                    slider.find( '.heading-slider-single-slide' ).find( '.heading-slider-single-slide-content' ).removeClass( 'animated animated-semi-speed fadeInRightSmall fadeOutLeftSmall' );

                    slider.find( '.slider-navigation-dots' ).removeClass( 'proceed' );

                }, 800 );

            }, 400 );

        }, 100 );

    };

   /**
    *
    * action after click on images slider navigation
    *
    */

    $( 'body' ).on( 'click touchstart', 'section.heading-slider .slider-navigation-dots li', function( event ) {

        event.preventDefault();

        var element = $( this );
        var slider = element.parent().parent();
        var navigation = element.parent();
        var intervalTime = slider.data( 'interval' );
        var sliderID = slider.data( 'slider-id' );
        var slideID = element.data( 'slide-id' );
        var slidesCount = slider.find( '.slider-navigation-dots' ).children( 'li' ).length;

        if( typeof intervalTime == 'undefined' || intervalTime === null || intervalTime === false ) intervalTime = 6000;
        if( !navigation.hasClass( 'proceed' ) && !element.children().hasClass( 'slider-navigation-dot-active' ) && ( slidesCount > 1 ) ) {

            element.siblings( 'li' ).children( '.slider-navigation-dot' ).removeClass( 'slider-navigation-dot-active' );
            element.children( '.slider-navigation-dot' ).addClass( 'slider-navigation-dot-active' );

            clearInterval( martanianOakHouseIntervals['heading-slider-'+ sliderID] );
            $.martanianOakHouseSwitchHeadingSlide( slider, 'find', slideID );

            setTimeout( function() {

                if( intervalTime !== 0 ) {

                    martanianOakHouseIntervals['heading-slider-'+ sliderID] = setInterval( function() {

                        $.martanianOakHouseSwitchHeadingSlide( slider, 'find', 'next' );

                    }, parseInt( intervalTime, 10 ) );
                }

            }, 300 );
        }

    });

   /**
    *
    * isotope
    *
    */

    $.martanianOakHouseConfigureIsotope = function() {

        var columnWidthValue = 0;
        switch( parseInt( $( 'section.gallery > .container' ).css( 'width' ), 10 ) ) {

            case 1140: columnWidthValue = 390; break;
            case 940: columnWidthValue = 323; break;
            case 720: columnWidthValue = 375; break;
            default: columnWidthValue = 0; break;
        }

        $( '.isotope-grid' ).isotope({
            itemSelector: '.isotope-grid-item',
            layoutMode: 'masonry',
            masonry: { columnWidth: columnWidthValue }
        });

    };

   /**
    *
    * configure references
    *
    */

    $.martanianOakHouseConfigureReferences = function() {

        var sliderID = 1;
        $( 'section.references' ).each( function() {

            var slider = $( this );
            var referencesSlider = slider.find( '.references-slider' );

            slider.data( 'slider-id', sliderID ).attr( 'data-slider-id', sliderID );

           /**
            *
            * set id for single slide and show / hide each one
            *
            */

            var referenceID = 1;
            referencesSlider.find( '.single-reference' ).each( function() {

                var reference = $( this );

                if( referenceID != 1 ) reference.css({ 'display': 'none' });
                else reference.addClass( 'active' );

                if( referencesSlider.find( '.single-reference' ).length > 1 ) reference.attr( 'data-slide-id', referenceID );

                referenceID++;

            });

           /**
            *
            * configure navigation
            *
            */

            if( referenceID > 2 ) {

                var navigation = '';
                for( var i = 1; i < referenceID; i++ ) {

                    navigation += '<li data-slide-id="'+ i +'"><span class="slider-navigation-dot '+ ( i == 1 ? 'slider-navigation-dot-active' : '' ) +'"></span></li>';
                }

                slider.append( '<ul class="slider-navigation-dots">'+ navigation +'</ul>' );
            }

           /**
            *
            * run the slider
            *
            */

            var intervalTime = slider.data( 'interval' );
            if( typeof intervalTime == 'undefined' || intervalTime === null || intervalTime === false ) intervalTime = 6000;

            if( intervalTime !== 0 ) {

                martanianOakHouseIntervals['references-'+ sliderID] = setInterval( function() {

                    $.martanianOakHouseSwitchReference( slider, referencesSlider.find( '.single-reference' ).length, 'next' );

                }, parseInt( intervalTime, 10 ) );
            }

           /**
            *
            * increase slider id flag
            *
            */

            sliderID++;

           /**
            *
            * end of function.
            *
            */

        });

    };

   /**
    *
    * switch references slider
    *
    */

    $.martanianOakHouseSwitchReference = function( slider, referencesCount, referenceID ) {

        slider.find( '.slider-navigation-dots' ).addClass( 'proceed' );
        var currentReferenceID = slider.find( '.single-reference.active' ).data( 'slide-id' );

        if( referencesCount == 'find' ) referencesCount = slider.children( '.slider-navigation-dots' ).children( 'li' ).length;
        if( referenceID == 'next' ) referenceID = currentReferenceID + 1 > referencesCount ? 1 : currentReferenceID + 1;

        var currentSlide = slider.find( '.single-reference[data-slide-id="'+ currentReferenceID +'"]' );
        var newSlide = slider.find( '.single-reference[data-slide-id="'+ referenceID +'"]' );

        currentSlide.removeClass( 'active' ).addClass( 'animated fadeOutDownSmall' );
        setTimeout( function() {

            newSlide.css({ 'display': 'block' }).addClass( 'active animated fadeInDownSmall' );

            slider.find( '.slider-navigation-dots' ).children( 'li[data-slide-id="'+ currentReferenceID +'"]' ).children( '.slider-navigation-dot' ).removeClass( 'slider-navigation-dot-active' );
            slider.find( '.slider-navigation-dots' ).children( 'li[data-slide-id="'+ referenceID +'"]' ).children( '.slider-navigation-dot' ).addClass( 'slider-navigation-dot-active' );

            setTimeout( function() {

                currentSlide.css({ 'display': 'none' }).removeClass( 'animated fadeOutDownSmall' );
                newSlide.removeClass( 'animated fadeInDownSmall' );

                slider.find( '.slider-navigation-dots' ).removeClass( 'proceed' );

            }, 900 );

        }, 300 );

    };

   /**
    *
    * action after click on images slider navigation
    *
    */

    $( 'body' ).on( 'click touchstart', 'section.references .slider-navigation-dots li', function( event ) {

        event.preventDefault();

        var element = $( this );
        var slider = element.parents( 'section.references' );
        var navigation = element.parent();
        var intervalTime = slider.data( 'interval' );
        var sliderID = slider.data( 'slider-id' );
        var referenceID = element.data( 'slide-id' );
        var sliderReferencesCount = slider.find( '.slider-navigation-dots' ).children( 'li' ).length;

        if( typeof intervalTime == 'undefined' || intervalTime === null || intervalTime === false ) intervalTime = 6000;
        if( !navigation.hasClass( 'proceed' ) && !element.children().hasClass( 'slider-navigation-dot-active' ) && ( sliderReferencesCount > 1 ) ) {

            element.siblings( 'li' ).children( '.slider-navigation-dot' ).removeClass( 'slider-navigation-dot-active' );
            element.children( '.slider-navigation-dot' ).addClass( 'slider-navigation-dot-active' );

            clearInterval( martanianOakHouseIntervals['references-'+ sliderID] );
            $.martanianOakHouseSwitchReference( slider, 'find', referenceID );

            setTimeout( function() {

                if( intervalTime !== 0 ) {

                    martanianOakHouseIntervals['references-'+ sliderID] = setInterval( function() {

                        $.martanianOakHouseSwitchReference( slider, 'find', 'next' );

                    }, parseInt( intervalTime, 10 ) );
                }

            }, 300 );
        }

    });

   /**
    *
    * configure images header section heights
    *
    */

    $.martanianOakHouseConfigureImagesHeaderSection = function() {

        $( 'section.images-header' ).each( function() {

            var section = $( this );
            var leftColumn = section.find( '.col-md-6' ).first();
            var rightColumn = section.find( '.col-md-6' ).last();
            var elements = {
                'firstImages': leftColumn.children( '.images' ),
                'secondImages': leftColumn.children( '.images-header-bottom' ).children( '.images' ),
                'content': leftColumn.children( '.images-header-bottom' ).children( '.content' )
            };

            var contentHeight = parseInt( elements.content.css( 'height' ), 10 );
            var sectionHeight = parseInt( rightColumn.css( 'height' ), 10 );

            if( leftColumn.css( 'float' ) != 'none' ) {

                elements.secondImages.css({ 'height': contentHeight });
                elements.firstImages.css({ 'height': sectionHeight - contentHeight - parseInt( elements.firstImages.css( 'margin-bottom' ), 10 ) });
            }

            else {

                elements.secondImages.css({ 'height': '' });
                elements.firstImages.css({ 'height': '' });
            }

        });
    };

   /**
    *
    * configure progress bars
    *
    */

    $.martanianOakHouseConfigureProgressBars = function() {

        $( 'section.circle-progress-elements' ).each( function() {

            var section = $( this );
            section.find( '.circle-progress-element' ).each( function() {

                var progressBarElement = $( this );
                progressBarElement.append( '<span class="value"></span>' );

                progressBarElement.circleProgress({

                    value: progressBarElement.data( 'progress-bar-value' ),
                    fill: { gradient: ["#ea7512", '#f19a15', "#e1490f"] },
                    size: 140.0
                })

                progressBarElement.on( 'circle-animation-progress', function( event, progress, stepValue ) {

                    var value = parseInt( String( stepValue.toFixed( 2 ) ).substr( 2 ), 10 );
                    $( this ).find( 'span.value' ).html( value +'%' );

                });

            });

        });

    };

   /**
    *
    * configure images heights
    *
    */

    $.martanianOakHouseConfigureImagesHeights = function() {

        $( 'section.content-with-image-on-left-side, section.content-with-image-on-right-side' ).each( function() {

            var section = $( this );
            var images = section.find( '.col-md-4' ).children( '.images' );
            var content = section.find( '.col-md-4' ).children( '.content' );
            var isMobile = content.parents( '.col-md-4' ).css( 'display' ) == 'block' && content.parents( '.col-md-4' ).css( 'float' ) == 'none';

            if( isMobile == false ) images.css({ 'height': parseInt( content.css( 'height' ), 10 ) });
            else images.css({ 'height': '' });

        });
    };

   /**
    *
    * configure google maps
    *
    */

    $.martanianOakHouseConfigureGoogleMaps = function() {

        var mapID = 1;
        $( '.location-details-map' ).each( function() {

            var mapBox = $( this );
            var lat = mapBox.data( 'lat' );
            var lng = mapBox.data( 'lng' );
            var zoomedOut = false;
            var zoom = mapBox.data( 'zoom-level' );
            var contentSize = parseInt( mapBox.parents( 'section.location-details' ).css( 'width' ), 10 );

            if( contentSize < 690 && zoom > 1 ) {

                zoom = zoom - 1;
                zoomedOut = true;
            }

            mapBox.attr( 'id', 'google-map-'+ mapID );

            var map = new google.maps.Map( document.getElementById( 'google-map-'+ mapID ), {
                zoom: zoom,
                center: new google.maps.LatLng( lat, lng ),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                scrollwheel: false,
                styles: [{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"on"},{"saturation":-100},{"lightness":20}]},{"featureType":"road","elementType":"all","stylers":[{"visibility":"on"},{"saturation":-100},{"lightness":40}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"saturation":-10},{"lightness":30}]},{"featureType":"landscape.man_made","elementType":"all","stylers":[{"visibility":"simplified"},{"saturation":-60},{"lightness":10}]},{"featureType":"landscape.natural","elementType":"all","stylers":[{"visibility":"simplified"},{"saturation":-60},{"lightness":60}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"},{"saturation":-100},{"lightness":60}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"},{"saturation":-100},{"lightness":60}]}]
            });

            mapBox.siblings( '.location-details-map-marker' ).each( function() {

                var markerLat = $( this ).data( 'lat' );
                var markerLng = $( this ).data( 'lng' );
                var markerType = $( this ).data( 'type' );

                new google.maps.Marker({
                    position: new google.maps.LatLng( markerLat, markerLng ),
                    map: map
                });

            });

            google.maps.event.addDomListener( window, 'resize', function() {

                var mapCenter = map.getCenter();

                google.maps.event.trigger( map, 'resize' );
                map.setCenter( mapCenter );

               /**
                *
                * zoom-in and zoom-out for map
                *
                */

                var currentZoom = map.getZoom();
                contentSize = parseInt( mapBox.parents( 'section.location-details' ).css( 'width' ), 10 );

                if( contentSize < 690 && zoomedOut == false ) {

                    map.setZoom( currentZoom - 1 );
                    zoomedOut = true;
                }

                else if( contentSize >= 690 && zoomedOut == true ) {

                    map.setZoom( currentZoom + 1 );
                    zoomedOut = false;
                }

            });

            mapID++;

        });

    };

   /**
    *
    * configure selects
    *
    */

    $.martanianOakHouseConfigureSelects = function() {

        $( 'select' ).each( function() {

            var select = $( this );
            select.wrap( '<span class="select"></span>' );

        });

    };

   /**
    *
    * configure checkbox
    *
    */

    $.martanianOakHouseConfigureCheckbox = function() {

        $( '.checkbox-box' ).each( function() {

            var checkbox = $( this );
            var checked = checkbox.attr( 'data-checked' ) == 'yes' ? true : false;

            if( checked == true ) checkbox.children( '.checkbox-status' ).html( '<i class="fa fa-check"></i>' );
            else checkbox.children( '.checkbox-status' ).html( '' );

        });

    };

   /**
    *
    * checkbox field change
    *
    */

    $( 'body' ).on( 'click touchstart', '.checkbox-box', function( event ) {

        event.preventDefault();
        var target = $( event.target );

        if( target.is( 'a' ) === false ) {

            var checkbox = $( this );
            var checked = checkbox.attr( 'data-checked' ) == 'yes' ? true : false;

            if( checked == true ) {

                checkbox.attr( 'data-checked', 'no' ).data( 'checked', 'no' );
                checkbox.children( '.checkbox-status' ).html( '' );
            }

            else {

                checkbox.attr( 'data-checked', 'yes' ).data( 'checked', 'yes' );
                checkbox.children( '.checkbox-status' ).html( '<i class="fa fa-check"></i>' );
            }
        }

    });

   /**
    *
    * configure date fields
    *
    */

    $.martanianOakHouseConfigureDateFields = function() {

        $( 'input[type="date"]' ).each( function() {

            var field = $( this );
            field.wrap( '<span class="date-field"></span>' );

            field.parents( '.date-field' ).prepend( '<span class="date-field-icon"><i class="fa fa-calendar"></i></span>' );

        });

    };

   /**
    *
    * is form field required?
    *
    */

    $.martanianOakHouseIsFieldRequired = function( field ) {

        var required = field.data( 'required' );
        return( typeof required == 'undefined' || required == false || required == null || required == 'yes' ? true : false );

    };

   /**
    *
    * send form
    *
    */

    $( 'body' ).on( 'click touchstart', '.form-send', function( event ) {

        event.preventDefault();

        var form = $( this ).parents( 'form.form-active' );
        var fields = [];
        var isError = false;
        var formOptions = {
            'client-name-field': form.data( 'client-name-field' ),
            'client-email-field': form.data( 'client-email-field' ),
            'title': form.data( 'title' )
        };

        form.find( '.form-field' ).each( function() {

            var field = $.martanianOakHouseIsFormFieldValid( $( this ) );

            if( field !== false ) fields[fields.length] = field;
            else isError = true;

        });

        if( isError == false ) {

            var thanksLay = form.children( '.thanks-lay' );
            thanksLay.fadeIn( 300 );

            $.ajax({ url: '_assets/_php/submit.php',
                     data: { 'fields': fields, 'options': formOptions },
                     type: 'post',
                     success: function( output ) {

                         var layClass = output == 'OK' ? '.thanks-lay-content-sent' : '.thanks-lay-content-not-sent';

                         thanksLay.find( '.thanks-lay-content-sending' ).css({ 'display': 'none' });
                         thanksLay.find( layClass ).fadeIn( 300 );

                     },
                     error: function( output ) {

                         thanksLay.find( '.thanks-lay-content-sending' ).css({ 'display': 'none' });
                         thanksLay.find( '.thanks-lay-content-not-sent' ).fadeIn( 300 );

                     }});
        }

    });

   /**
    *
    * is form field valid
    *
    */

    $.martanianOakHouseIsFormFieldValid = function( field ) {

        var fieldName = field.attr( 'name' );
        var fieldValue = field.val();
        var fieldRequired = $.martanianOakHouseIsFieldRequired( field );

        if( typeof fieldName == 'undefined' ) fieldName = field.data( 'field-name' );
        if( ( typeof fieldValue == 'undefined' || fieldValue == null || fieldValue == false || fieldValue == '' ) && !field.is( 'input[type="text"], input[type="email"], input[type="password"], input[type="url"], input[type="tel"], input[type="number"], input[type="date"], textarea' ) ) {

            if( field.hasClass( 'checkbox-box' ) ) {

                var checked = field.data( 'checked' );
                fieldValue = fieldRequired == false || ( fieldRequired == true && checked == 'yes' ) ? field.data( 'value-if-checked' ) : '';
            }
        }

        if( ( fieldRequired == true && fieldValue != '' ) || fieldRequired == false ) {

            if( field.is( 'select' ) ) field.parent().removeClass( 'error' );
            else field.removeClass( 'error' );
        }

        else {

            if( field.is( 'select' ) ) field.parent().addClass( 'error' );
            else field.addClass( 'error' );

            return false;
        }

        return( { 'name': fieldName, 'value': fieldValue } );
    };

   /**
    *
    * close thanks-lay notice
    *
    */

    $( 'body' ).on( 'click touchstart', '.thanks-lay-close', function( event ) {

        event.preventDefault();

        var thanksLay = $( this ).parents( '.thanks-lay' );
        thanksLay.fadeOut( 300 );

        setTimeout( function() {

            thanksLay.find( '.thanks-lay-content-sent' ).css({ 'display': 'none' });
            thanksLay.find( '.thanks-lay-content-not-sent' ).css({ 'display': 'none' });

        }, 300 );

    });

   /**
    *
    * play the video
    *
    */

    $( 'body' ).on( 'click touchstart', 'section.video .video-play-button', function( event ) {

        event.preventDefault();

        var section = $( this ).parents( 'section.video' );
        var videoURL = section.data( 'video-url' );

        $.magnificPopup.open({
          		type: 'iframe',
            items: {
                src: videoURL
            }
       	});

    });

   /**
    *
    * change menu visibility flag
    *
    */

    $.martanianOakHouseChangeResponsiveMenuVisibilityFlag = function( visibility ) {

        martanianOakHouseResponsiveMenuVisible = visibility;

    };

   /**
    *
    * configure responsive menu
    *
    */

    $.martanianOakHouseConfigureResponsiveMenu = function() {

        var contentSize = parseInt( $( 'header.header-bar .container' ).css( 'width' ), 10 );
        var responsiveMenuWidth = contentSize < 750 ? ( contentSize <= 370 ? 180 : 250 ) : 300;

        var headerBar = $( 'header' );
        var headerMenu = headerBar.find( 'ul.menu' );
        var headerTopBar = headerBar.find( '.header-bar-top' );

        martanianOakHouseResponsiveMenuVisible = false;

        headerBar.css({ 'left': '0' });
        $( '.big-wrapper' ).css({ 'margin-left': '', 'width': '' });
        $( '.responsive-menu-content' ).css({ 'display': 'none', 'right': '-'+ responsiveMenuWidth +'px' });

        if( contentSize >= 970 ) $( '.responsive-menu-content' ).remove();
        else {

            if( $( '.responsive-menu-content' ).length == 0 ) {

                $( 'body' ).append( '<div class="responsive-menu-content"></div>' );
                $( '.responsive-menu-content' ).append( '<ul class="menu">'+ headerMenu.html() +'</ul>'+ headerTopBar.html() );
                $( '.responsive-menu-content' ).find( '.sub-menu' ).removeClass( 'animated animated-speed fadeInDown' );

                $( '.responsive-menu-content .header-bar-top-element[data-element-type="phone"]' ).prepend( '<i class="fa fa-phone"></i>' );
                $( '.responsive-menu-content .header-bar-top-element[data-element-type="email"]' ).prepend( '<i class="fa fa-envelope-o"></i>' );
                $( '.responsive-menu-content .header-bar-top-element[data-element-type="location"]' ).prepend( '<i class="fa fa-map-marker"></i>' );
                $( '.responsive-menu-content .header-bar-top-element[data-element-type="languages"]' ).prepend( '<i class="fa fa-globe"></i>' );

                $( '.responsive-menu-content .header-bar-top-element[data-element-type="languages"] i.fa-caret-down' ).remove();
            }
        }
    };

   /**
    *
    * show responsive menu
    *
    */

    $( 'body' ).on( 'click touchstart', '.responsive-menu-button', function( event ) {

        event.preventDefault();

        var contentSize = parseInt( $( 'header.header-bar .container' ).css( 'width' ), 10 );
        var responsiveMenuWidth = contentSize < 750 ? ( contentSize <= 370 ? 180 : 250 ) : 300;

        if( martanianOakHouseResponsiveMenuVisible == false ) {

            var wrapper = $( '.big-wrapper' );
            var wrapperWidth = wrapper.width();
            var headerBar = $( this ).parents( 'header.header-bar' );

            headerBar.animate({ 'left': '-'+ responsiveMenuWidth +'px' }, 300 );
            wrapper.animate({ 'margin-left': '-'+ responsiveMenuWidth +'px', 'width': wrapperWidth }, 300 );

            $( '.responsive-menu-content' ).css({ 'display': 'block' }).animate({ 'right': '0' }, 300 );
            martanianOakHouseResponsiveMenuVisible = true;
        }

        else {

            var wrapper = $( '.big-wrapper' );
            var wrapperWidth = wrapper.width();
            var headerBar = $( this ).parents( 'header.header-bar' );

            headerBar.animate({ 'left': '0' }, 300 );
            wrapper.animate({ 'margin-left': '0' }, 300 );

            $( '.responsive-menu-content' ).css({ 'display': 'block' }).animate({ 'right': '-'+ responsiveMenuWidth +'px' }, 300 );

            setTimeout( function() {

                $( '.responsive-menu-content' ).css({ 'display': 'none' });
                wrapper.css({ 'margin-left': '', 'width': '' });
                headerBar.css({ 'left': '' });

            }, 300 );

            martanianOakHouseResponsiveMenuVisible = false;
        }

    });

   /**
    *
    * configure contact form backgrounds
    *
    */

    $.martanianOakHouseConfigureContactFormBackgrounds = function() {

        $( 'section.contact-form' ).each( function() {

            var section = $( this );
            var formBackground = section.find( '.contact-form-background' );
            var imageBackground = section.find( '.contact-form-background-image' );
            var form = section.find( '.contact-form-box' );
            var formHeight = parseInt( form.css( 'height' ), 10 );
            var isMobile = section.find( '.col-md-6' ).css( 'float' ) == 'none';

            if( isMobile == false ) {

                formBackground.css({ 'height': formHeight });
                imageBackground.css({ 'height': formHeight });
            }

            else {

                formBackground.css({ 'height': formHeight });
                imageBackground.css({ 'height': 350 });
            }

        });
    }

   /**
    *
    * configure heading slider content for mobile
    *
    */

    $.martanianOakHouseConfigureHeadingSliderContentForMobile = function( animate ) {

        $( 'section.heading-slider' ).each( function() {

            var slider = $( this );
            var currentSlide = slider.find( '.heading-slider-single-slide.active' );
            var currentSlideContent = currentSlide.find( '.heading-slider-single-slide-content' );
            var isMobile = currentSlideContent.css( 'display' ) == 'block';

            if( isMobile == true ) {

                var height = parseInt( currentSlideContent.css( 'height' ), 10 );

                if( animate == false ) slider.css({ 'margin-bottom': height });
                else slider.animate({ 'margin-bottom': height }, 200 );

                if( slider.find( '.heading-slider-background-overlay' ).length == 0 ) slider.append( '<div class="heading-slider-background-overlay"></div>' );
                slider.find( '.heading-slider-background-overlay' ).css({ 'height': height, 'bottom': '-'+ height +'px' });
            }

            else {

                slider.css({ 'margin-bottom': '' });
                slider.find( '.heading-slider-background-overlay' ).remove();
            }

        });
    };

   /**
    *
    * function returns an image URL from background css attribute
    *
    */

    $.martanianOakHouseGetImageURL = function( image ) {

        var backgroundURL = /^url\((['"]?)(.*)\1\)$/.exec( image );
        return( backgroundURL ? backgroundURL[2] : false );
    };

   /**
    *
    * configure images for magnific popup
    *
    */

    $.martanianOakHouseConfigureImagesForMagnificPopup = function() {

        $( '.images' ).each( function() {

            var images = $( this );
            if( images.parents( '.widget' ).length == 0 ) {

                images.find( '.image' ).each( function() {

                    var image = $( this );
                    var imageURL = $.martanianOakHouseGetImageURL( image.css( 'background-image' ) );

                    image.data( 'mfp-src', imageURL ).attr( 'data-mfp-src', imageURL );
                    image.html( '<div class="image-caption"><div class="image-caption-icon"><i class="fa fa-expand"></i></div></div>' );

                });

                images.magnificPopup({
                    delegate: '.image',
                    type: 'image',
                    gallery: { enabled: true }
                });
            }

        });

        $( 'section.gallery' ).each( function() {

            var gallery = $( this );
            gallery.find( '.isotope-grid-item' ).each( function() {

                var image = $( this );
                var imageURL = $.martanianOakHouseGetImageURL( image.css( 'background-image' ) );

                image.data( 'mfp-src', imageURL ).attr( 'data-mfp-src', imageURL );
                image.html( '<div class="image-caption"><div class="image-caption-icon"><i class="fa fa-expand"></i></div></div>' );

            });

            gallery.magnificPopup({
                delegate: '.isotope-grid-item',
                type: 'image',
                gallery: { enabled: true }
            });

        });
    };

   /**
    *
    * end of file.
    *
    */

});