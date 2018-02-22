% Transistion matrix
T = [0.7 0.3;
     0.3 0.7];
% Sensor matrices 
Ot = [0.9 0.0;
      0.0 0.2];

Of = [0.1 0.0;
      0.0 0.8];

%Initial value: chance of rain with no prior knowledge
f0 =[0.5 0.5]';
  
  
% Normalize
n = @(matrix) (matrix./sum(sum(matrix)));


% Forward filtering eq 15.12
forward_filter = @(T,O,f_prev)(n(O*T'*f_prev));


%Task B
evidence_B1 = [1 1]; % Umbrella used on day 1 and 2
f = f0; % Set to apriori probability distribution
for i = 1:length(evidence_B)
    if evidence_B[i] == 1;
        f = forward_filter(T,Ot,f);
    else
        f = forward_filter(T,Of,f);
    end
end
fprintf('TASK B1: Evidence: <%i, %i> , Probability of rain: %f\n',evidence_B,f(1));

evidence_B2 = [1 1 0 1 1];
n = length(evidence_B2);

f = zeros(2,n);
f(:,1) = [0.5,0.5]';
for i = 1:n
    if evidence_B[i] == 1;
        f(:,i+1) = forward_filter(T,Ot,f(:,i));
    else
        f(:,i+1) = forward_filter(T,Of,f(:,i));
    end
    
    fprintf('f%i = <%4f, %f4>\n',i,f(1,i),f(2,i));
end


