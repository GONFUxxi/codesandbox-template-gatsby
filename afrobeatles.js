import { setProcessing, getPriceDollars } from "./common.js";

/**
 * Generates a row for the leaderboard table displaying the fan's name 
 * and total amount sold. 
 * @param {string} name - the sellers name
 * @param {string} amount - the total amount sold through their Payment Link 
 * @returns A div generated from the template element within the leaderboard.html. 
 */
const showLeaderBoardRow = function ({ name, amount }) {
  //use template to create a div for the given
  const price = getPriceDollars(amount, true);
  const rowTemplate = document.querySelector('#seller-summary');
  const rowDiv = rowTemplate.content.firstElementChild.cloneNode(true);
  let nameDiv = rowDiv.getElementsByClassName('summary-name')[0];
  nameDiv.textContent = name;
  let priceDiv = rowDiv.getElementsByClassName('summary-sale')[0];
  priceDiv.textContent = price;
  return rowDiv;
}

/**
 * Builds the leaderboard table, generating a row for each seller. 
 * @param {} sellers 
 */
const showSellers = function (sellers) {
  let sellerTable = document.getElementById("summary-table");
  sellers.forEach((seller) => {
    let row = showLeaderBoardRow({
      name: seller.name,
      email: seller.email,
      amount: seller.amount
    });
    sellerTable.append(row);
  });
}

/**
 * Shows the leaderboard.html page by 
 */
const showPage = async function (){
  /** 
   * TODO: Integrate Stripe
   * Milestone 2: Complete this function to display the leaderboard of sellers. 
   */
}

/**
 * Make call to server to get sorted leaderboard
  * @returns {Array} sellers - Returns Seller array with name, email, and total amount that is sorted desc by total amount
 */
const getLeaderboard = async () => {
  /** 
   * TODO: Integrate Stripe
   * Milestone 2: complete this function to fetch the fans to display on the 
   * leaderboard. 
   */
};

window.addEventListener('DOMContentLoaded', (event) => {
  showPage();
});

import {emailPattern, setProcessing} from "./common.js";

/**
 * Handle the user completing the registration form. 
 */
const handleClick = async function (event)
{
  event.preventDefault();
  /** 
   * TODO: Integrate Stripe
   * Milestone 1: Complete this function to return a payment for the fan 
   * once they have filled out the registration form. Their email and display name 
   * are both required.  
   * 
   * You can use the setProcessing() in common.js
   * to help control the UX during calls to the server, and setError() to display
   * any errors. 
   * 
   * After you've received the Payment Link from the server 
   * call showSignupComplete to display the seller's Payment Link.  
   */
}

/** 
 * Helper function to show an error message on the page. 
 * @param {string} errorMsg - msg to be displayed
 */
const setError = function (errorMsg) {
  const errDiv = document.getElementById('paymentlink-error');
  const messageElement = errDiv.getElementsByTagName("p")[0];
  messageElement.textContent = errorMsg;
  errDiv.style.display = 'block';
}

/**
 * @returns the Payment Link displayed on the page. 
 */
const getPaymentLink = function () {
  let paymentLinkDisplay = document.getElementById("payment-link");
  return paymentLinkDisplay.textContent;
}

/**
 * Displays the provided Payment Link 
 * @param {string} paymentLinkUrl
 */
const setPaymentLink = function (paymentLinkUrl) {
  let paymentLinkDisplay = document.getElementById("payment-link");
  paymentLinkDisplay.textContent = paymentLinkUrl;
}

/**
 * Replaces the registration form with a sign up complete message
 * and the seller's Payment Link. 
 * @param {string} paymentLinkUrl 
 */
const showSignupComplete = function (paymentLinkUrl) {
  setPaymentLink(paymentLinkUrl);
  togglePaymentLinkDiv(true);
  let formWrapper = document.getElementById("form-div");
  formWrapper.style.display = "none";
}

/**
 * Toggles the div showing a Payment Link either showing or hidding it. 
 * @param {boolean} display 
 */
const togglePaymentLinkDiv = function (display) {
  let paymentLinkWrapper = document.getElementById("paymentlink-wrapper");
  if (display) {
    paymentLinkWrapper.style.display = "block";
    paymentLinkWrapper.scrollIntoView();
  } else {
    paymentLinkWrapper.style.display = "none";
  }
}

/**
 * Copy the Payment Link to the clipboard. 
 */
 const copyToClipboard = async () => {
  const paymentLink = getPaymentLink();
  navigator.clipboard.writeText(paymentLink);
};

window.addEventListener('DOMContentLoaded', (event) => {
  togglePaymentLinkDiv(false);
  const submitBtn = document.getElementById('submit');
  submitBtn.addEventListener('click', handleClick);
  const emailInput = document.getElementById('email');
  emailInput.setAttribute('pattern', emailPattern);
  const clipboardBtn = document.getElementById('copy-button');
  clipboardBtn.addEventListener('click', copyToClipboard);
  const errorDivs = document.getElementById('paymentlink-error');
  errorDivs.style.display = 'none';
});


