<?php

   /**
    *
    * submit contact form or appointment form
    * to your email address
    *
    * @author: Martanian <support@martanian.com>
    *
    */

    # put your name here
    define( 'OWNER_NAME', 'Your name' );

    # put your email address here
    define( 'OWNER_EMAIL', 'your-email@example.com' );

    # put your do-not-reply email address here
    define( 'DO_NOT_REPLY_EMAIL', 'no-reply@example.com' );

   /**
    *
    * create email content and reply-to
    *
    */

    # not for direct entry
    if( !isset( $_POST ) || !isset( $_POST['fields'] ) || !isset( $_POST['options'] ) ) exit;

    # define "reply" array
    $reply = array(
        'name' => '',
        'email' => ''
    );

    # search for client "name" and "email" fields
    foreach( $_POST['fields'] as $field ) {

        # client name?
        if( $reply['name'] == '' && $field['name'] == $_POST['options']['client-name-field'] ) $reply['name'] = $field['value'];

        # client mail?
        if( $reply['email'] == '' && $field['name'] == $_POST['options']['client-email-field'] ) $reply['email'] = $field['value'];
    }

   /**
    *
    * headers
    *
    */

    # email headers
    $headers = "MIME-Version: 1.0\n".
               "Content-type: text/html; charset=utf-8\n".
               "Content-Transfer-Encoding: 8bit\n".
               "From: ". OWNER_NAME ." <". DO_NOT_REPLY_EMAIL .">\n".
               "Reply-to: ". $reply['name'] ." <". $reply['email'] .">\n".
               "Date: ". date( "r" ). "\n";

   /**
    *
    * contents
    *
    */

    # non-html content
    $nonHTML = '';

    # create rows with values from appointment form
    $rows = '';
    foreach( $_POST['fields'] as $field ) {

        # html rows
        $rows .= '<tr>

                      <td style="width: 200px; font-weight: bold; border: 1px solid #eee; padding: 10px;">'. $field['name'] .'</td>
                      <td style="border: 1px solid #eee; padding: 10px;">'. $field['value'] .'</td>

                  </tr>';

        # non-html rows
        $nonHTML .= $field['name'] ."\n". $field['value'] ."\n\n";
    }

    # email content
    $content = '<table style="width: 600px; font-size: 11px; border-collapse: collapse;">'. $rows .'</table>';

   /**
    *
    * sending
    *
    */

    # sending an email
    $resultHTML = mail(
        OWNER_EMAIL,
        "=?UTF-8?B?". base64_encode( $_POST['options']['title'] ) ."?=",
        $content,
        $headers
    );

    # if the email wasn't send
    if( $resultHTML == false ) {

        # second version of email
        $resultNonHTML = mail(
            OWNER_EMAIL,
            "=?UTF-8?B?". base64_encode( $_POST['options']['title'] ) ."?=",
            $nonHTML
        );

        # wasn't send?
        if( $resultNonHTML == false ) exit( 'WRONG' );
    }

    # ok
    exit( 'OK' );

   /**
    *
    * end of file
    *
    */

?>