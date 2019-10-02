/* eslint-disable func-names */
/* eslint-disable prefer-arrow-callback */


function youtube_parser(url) {
  const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[7].length == 11) ? match[7] : false;
}


$(document).ready(function () {
  console.log('loaded');
  $('#url').change(function () {
    const youtube_id = youtube_parser($('#url').val());
    if (youtube_id) {
      $.ajax({
        url: `https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=${  youtube_id  }&key=AIzaSyD8zLRxL3sMpldE_F2PKs0du8PJJkYUJjA`,
        method: 'GET',
      }).done(function (res) {
        if ($('#title').val() === '') {
          $('#title').val(res.items[0].snippet.title);
        }
        if ($('#description').val() === '') {
          $('#description').val(res.items[0].snippet.description);
        }
      });
    }
  });
});
